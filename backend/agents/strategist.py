"""Strategist: FeatureCard + brand_card + stats -> ranked suggestions.

Deterministic ranker (`rank_strategies`) is the always-on scorer and the LLM
fallback. `run_strategist` tries the LLM (enum-constrained, structured output) and
falls back to the deterministic ranking on any failure.
"""
from __future__ import annotations

from backend.agents import guardrails, runtime
from backend.config import get_settings
from backend.learning import bias
from backend.schemas import BrandCard, FeatureCard, StrategistLLMOut, Suggestion
from backend.strategies import (
    StrategyId,
    as_id_desc_lines,
    brand_fit,
    library_ids,
    load_strategies,
)

_SYS = (
    runtime.GOAL + "\n\n"
    "You are the Strategist. Rank marketing strategies from the FIXED library below. "
    "Each suggestion's strategy_id MUST be one of the given ids. Keep rationale <=160 chars. "
    "Bias ranking by the feedback stats and any user feedback. "
    "Return ONLY the JSON object {\"suggestions\": [...]} ranked best-first."
)

# How strongly each strategy matches the audience signals (deterministic, 0..1).
_TITLES = {
    "loyalty": "Reward your loyal members",
    "discount": "Limited-time offer to convert",
    "social": "Amplify with social proof",
    "urgency": "Act-now, time-limited push",
    "welcome": "Warm welcome for new prospects",
    "winback": "Win back lapsed customers",
    "novelty": "Spotlight what's new",
}
_SIGNAL_NAMES = {
    "loyalty": "loyalty+engagement",
    "discount": "price sensitivity",
    "social": "engagement+novelty",
    "urgency": "price+recency",
    "welcome": "new audience",
    "winback": "low recency",
    "novelty": "novelty",
}


def _target_score(sid: str, f) -> float:
    table = {
        "loyalty": (f.loyalty + f.engage) / 2,
        "discount": f.price_sens,
        "social": (f.engage + f.novelty) / 2,
        "urgency": (f.price_sens + f.recency) / 2,
        "welcome": 1.0 if f.is_new else 0.2,
        "winback": 1.0 - f.recency,
        "novelty": f.novelty,
    }
    return table[sid]


def _rationale(sid: str, fc: FeatureCard) -> str:
    return f"Targets {_SIGNAL_NAMES[sid]} for the '{fc.persona}' persona."[:160]


def rank_strategies(
    feature_card: FeatureCard,
    brand_card: BrandCard,
    stats_map: dict[str, dict],
    feedback: str | None = None,
) -> list[Suggestion]:
    fb = (feedback or "").lower()
    scored: list[tuple[float, Suggestion]] = []
    for strat in load_strategies():
        sid = strat["id"]
        fit = float(strat["brand_fit"])
        score = (
            0.45 * _target_score(sid, feature_card.f)
            + 0.30 * fit
            + 0.25 * bias(stats_map.get(sid))  # learning bias — weighted so feedback visibly re-ranks
        )
        if fb and (sid in fb or _SIGNAL_NAMES[sid].split("+")[0] in fb):
            score += 0.3  # nudge strategies the user's feedback mentions
        sug = Suggestion(
            strategy_id=StrategyId(sid),
            title=_TITLES[sid],
            rationale=_rationale(sid, feature_card),
            target_signal=_SIGNAL_NAMES[sid],
            on_brand=fit >= 0.5,
        )
        scored.append((score, sug))
    scored.sort(key=lambda x: x[0], reverse=True)
    return guardrails.guard_suggestions([s for _, s in scored], brand_card)


def _compact_input(fc: FeatureCard, brand: BrandCard, stats_lines: str, feedback: str | None) -> str:
    f = fc.f
    sig = (
        f"price_sens={f.price_sens} loyalty={f.loyalty} recency={f.recency} "
        f"novelty={f.novelty} engage={f.engage} is_new={f.is_new}"
    )
    parts = [
        f"persona: {fc.persona}",
        f"signals: {sig}",
        f"tags: {','.join(fc.tags)}",
        f"brand_tone: {brand.tone}",
        "strategies:",
        as_id_desc_lines(),
        f"stats_top3:\n{stats_lines}",
    ]
    if feedback:
        parts.append(f"user_feedback: {feedback[:200]}")
    return "\n".join(parts)


async def run_strategist(
    feature_card: FeatureCard,
    brand_card: BrandCard,
    stats_map: dict[str, dict],
    stats_lines: str = "none",
    feedback: str | None = None,
) -> list[Suggestion]:
    deterministic = rank_strategies(feature_card, brand_card, stats_map, feedback)
    if not get_settings().has_llm:
        return deterministic
    user_input = _compact_input(feature_card, brand_card, stats_lines, feedback)
    try:
        out: StrategistLLMOut | None = await runtime.run_structured(_SYS, user_input, StrategistLLMOut)
    except Exception:
        out = None
    if not out or not out.suggestions:
        return deterministic
    guarded = guardrails.guard_suggestions(_convert(out.suggestions, feature_card), brand_card)
    return guarded or deterministic


def _convert(items, feature_card: FeatureCard) -> list[Suggestion]:
    """Map tolerant LLM items to Suggestions: drop invalid ids (§8.1), truncate fields."""
    lib = library_ids()
    out: list[Suggestion] = []
    for s in items:
        sid = s.strategy_id.strip().lower()
        if sid not in lib:  # invalid strategy id -> drop the item
            continue
        out.append(
            Suggestion(
                strategy_id=StrategyId(sid),
                title=(s.title or _TITLES[sid])[:90],
                rationale=(s.rationale or _rationale(sid, feature_card))[:160],
                target_signal=s.target_signal or _SIGNAL_NAMES[sid],
                on_brand=brand_fit(sid) >= 0.5,
            )
        )
    return out
