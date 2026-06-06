"""Self-learning: approve/reject -> strategy_stats; read aggregates as a ranking bias.

Learning is DATA, not prompt: only top-3 aggregates flow to the Strategist, so the
context window stays flat no matter how many runs happen (spec: requirements.md §8.7).
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models_db import StrategyStat


async def record(session: AsyncSession, strategy_id: str, action: str) -> None:
    """Increment approvals/rejections for a strategy (upsert)."""
    stat = await session.get(StrategyStat, strategy_id)
    if stat is None:
        stat = StrategyStat(strategy_id=strategy_id, approvals=0, rejections=0)
        session.add(stat)
    if action == "approve":
        stat.approvals += 1
    else:
        stat.rejections += 1
    await session.commit()


async def stats_map(session: AsyncSession) -> dict[str, dict]:
    rows = (await session.execute(select(StrategyStat))).scalars().all()
    return {r.strategy_id: {"approvals": r.approvals, "rejections": r.rejections} for r in rows}


def top3_lines(smap: dict[str, dict]) -> str:
    """Compact top-3 aggregate lines for the Strategist prompt (never event logs)."""
    ranked = sorted(
        smap.items(),
        key=lambda kv: kv[1]["approvals"] - kv[1]["rejections"],
        reverse=True,
    )[:3]
    lines = [f"{sid}: +{v['approvals']}/-{v['rejections']}" for sid, v in ranked]
    return "\n".join(lines) if lines else "none"


def bias(stat: dict | None) -> float:
    """Map a strategy's net feedback to a small ranking bias in [-1, 1]."""
    if not stat:
        return 0.0
    net = stat["approvals"] - stat["rejections"]
    return max(-1.0, min(1.0, net / 5.0))
