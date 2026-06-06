"""Guardrails on every generated string (spec: requirements.md §8.4).

Reject on any brand restricted_keyword (case-insensitive), headline > 90 chars,
or body > 220 chars -> fall back to a safe template. `redact()` is a final safety
net that guarantees a restricted keyword never appears in any served output.
"""
from __future__ import annotations

import re

from backend.schemas import BrandCard, Suggestion
from backend.strategies import StrategyId

HEADLINE_MAX = 90
BODY_MAX = 220


def find_restricted(text: str, restricted: list[str]) -> str | None:
    low = text.lower()
    for kw in restricted:
        if kw and kw.lower() in low:
            return kw
    return None


def redact(text: str, restricted: list[str]) -> str:
    """Replace every restricted keyword with *** (case-insensitive)."""
    out = text
    for kw in restricted:
        if kw:
            out = re.sub(re.escape(kw), "***", out, flags=re.IGNORECASE)
    return out


def safe_suggestion(strategy_id: str, target_signal: str = "persona") -> Suggestion:
    return Suggestion(
        strategy_id=StrategyId(strategy_id),
        title=f"{strategy_id.capitalize()} outreach",
        rationale="On-brand suggestion generated from your audience signals.",
        target_signal=target_signal,
        on_brand=True,
    )


def guard_suggestion(sug: Suggestion, brand_card: BrandCard) -> Suggestion:
    restricted = brand_card.restricted_keywords
    if (
        find_restricted(sug.title, restricted)
        or find_restricted(sug.rationale, restricted)
        or len(sug.title) > HEADLINE_MAX
        or len(sug.rationale) > BODY_MAX
    ):
        return safe_suggestion(sug.strategy_id.value, sug.target_signal)
    return sug


def guard_suggestions(items: list[Suggestion], brand_card: BrandCard) -> list[Suggestion]:
    return [guard_suggestion(s, brand_card) for s in items]
