"""Assemble the downloadable spec files (deterministic templates) + final redaction.

Output files (spec: requirements.md §6): marketing-strategy-spec.md,
personalization-rules.json, brand-card.json. Every served string is redacted of
restricted keywords as a final safety net.
"""
from __future__ import annotations

import json

from backend.agents import guardrails
from backend.schemas import BrandCard, FeatureCard, SpecFile, Suggestion


def build_spec_files(
    feature_card: FeatureCard,
    brand_card: BrandCard,
    approved: list[Suggestion],
) -> list[SpecFile]:
    files = [
        SpecFile(
            name="marketing-strategy-spec.md",
            mime="text/markdown",
            content=_marketing_md(feature_card, brand_card, approved),
        ),
        SpecFile(
            name="personalization-rules.json",
            mime="application/json",
            content=_rules_json(feature_card, approved),
        ),
        SpecFile(
            name="brand-card.json",
            mime="application/json",
            content=_brand_json(brand_card),
        ),
    ]
    # Redact restricted keywords from marketing copy. brand-card.json legitimately
    # *lists* those keywords (it's the avoid-list), so it is left intact.
    restricted = brand_card.restricted_keywords
    for f in files:
        if f.name != "brand-card.json":
            f.content = guardrails.redact(f.content, restricted)
    return files


def _marketing_md(fc: FeatureCard, brand: BrandCard, approved: list[Suggestion]) -> str:
    lines = [
        "# Marketing Strategy Spec",
        "",
        f"**Persona:** {fc.persona}  ",
        f"**Brand tone:** {brand.tone}  ",
        f"**Tags:** {', '.join(fc.tags) or '—'}",
        "",
        "## Approved Strategies",
        "",
    ]
    if not approved:
        lines.append("_No strategies approved._")
    for i, s in enumerate(approved, 1):
        lines += [
            f"### {i}. {s.title}",
            f"- **Strategy:** `{s.strategy_id.value}`",
            f"- **Target signal:** {s.target_signal}",
            f"- **On-brand:** {'yes' if s.on_brand else 'review'}",
            f"- **Rationale:** {s.rationale}",
            "",
        ]
    return "\n".join(lines).rstrip() + "\n"


def _rules_json(fc: FeatureCard, approved: list[Suggestion]) -> str:
    payload = {
        "persona": fc.persona,
        "signals": fc.f.model_dump(),
        "rules": [
            {
                "strategy_id": s.strategy_id.value,
                "target_signal": s.target_signal,
                "title": s.title,
            }
            for s in approved
        ],
    }
    return json.dumps(payload, indent=2)


def _brand_json(brand: BrandCard) -> str:
    return json.dumps(brand.model_dump(), indent=2)
