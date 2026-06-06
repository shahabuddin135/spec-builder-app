"""Fixed strategy library (7) — the single source of truth for the strategy_id enum.

Library ids are a hard-coded constant (used for enum validation even when the seed
file is missing); descriptions and brand_fit are loaded from seed/strategies.json.
"""
from __future__ import annotations

import enum
import json
from functools import lru_cache
from pathlib import Path

_SEED_PATH = Path(__file__).resolve().parent / "seed" / "strategies.json"


class StrategyId(str, enum.Enum):
    """The only strategy ids any agent may emit. Invalid id -> item dropped."""

    loyalty = "loyalty"
    discount = "discount"
    social = "social"
    urgency = "urgency"
    welcome = "welcome"
    winback = "winback"
    novelty = "novelty"


@lru_cache
def load_strategies() -> list[dict]:
    """Load the 7 strategies from seed; validate ids match the StrategyId enum."""
    data = json.loads(_SEED_PATH.read_text(encoding="utf-8"))
    items = data["strategies"]
    seed_ids = {s["id"] for s in items}
    expected = {e.value for e in StrategyId}
    if seed_ids != expected:
        raise ValueError(
            f"strategies.json ids {seed_ids} do not match StrategyId {expected}"
        )
    return items


def library_ids() -> set[str]:
    """Set of valid strategy ids for enum constraint."""
    return {e.value for e in StrategyId}


def as_id_desc_lines() -> str:
    """Compact 'id: desc' lines for the Strategist prompt (never prose)."""
    return "\n".join(f"{s['id']}: {s['desc']}" for s in load_strategies())


def brand_fit(strategy_id: str) -> float:
    for s in load_strategies():
        if s["id"] == strategy_id:
            return float(s["brand_fit"])
    return 0.0
