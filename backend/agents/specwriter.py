"""Spec-Writer: approved suggestions + brand_card -> downloadable spec files.

The two JSON files are deterministic structured data. The Markdown spec may be
written by the LLM for nicer copy; on any failure it falls back to the deterministic
template. Every served string passes guardrails/redaction before it leaves.
"""
from __future__ import annotations

from backend import specgen
from backend.agents import guardrails, runtime
from backend.config import get_settings
from backend.schemas import BrandCard, FeatureCard, MarkdownOut, SpecFile, Suggestion

_MD_MAX_CHARS = 8000

_SYS = (
    runtime.GOAL + "\n\n"
    "You are the Spec-Writer. Write a concise, on-brand marketing strategy spec in Markdown "
    "from the approved suggestions and brand tone. Do NOT use any restricted keyword. "
    "Return ONLY the JSON object {\"markdown\": \"<string>\"}."
)


def _compact(fc: FeatureCard, brand: BrandCard, approved: list[Suggestion]) -> str:
    items = "; ".join(f"{s.strategy_id.value}:{s.title}" for s in approved)
    restricted = ", ".join(brand.restricted_keywords) or "none"
    return (
        f"persona: {fc.persona}\n"
        f"brand_tone: {brand.tone}\n"
        f"restricted_keywords: {restricted}\n"
        f"approved: {items}"
    )


async def run_specwriter(
    feature_card: FeatureCard,
    brand_card: BrandCard,
    approved: list[Suggestion],
) -> list[SpecFile]:
    files = specgen.build_spec_files(feature_card, brand_card, approved)
    if not get_settings().has_llm or not approved:
        return files

    try:
        out = await runtime.run_structured(_SYS, _compact(feature_card, brand_card, approved), MarkdownOut)
    except Exception:
        out = None

    if out and out.markdown.strip():
        md = guardrails.redact(out.markdown[:_MD_MAX_CHARS], brand_card.restricted_keywords)
        for f in files:
            if f.name.endswith(".md"):
                f.content = md
    return files
