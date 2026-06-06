"""Planner (Spec-Writer): ProjectBrief + answers -> enriched ProjectSpec.

The LLM fills out a complete, consistent spec object; `specgen` renders it into the
markdown file tree. The deterministic `specgen.deterministic_spec` is the fallback,
so a full spec package is always produced even with no model key.
"""
from __future__ import annotations

from backend import specgen
from backend.agents import runtime
from backend.config import SPEC_MAX_OUTPUT_TOKENS, get_settings
from backend.schemas import ProjectBrief, ProjectSpec

_SYS = (
    runtime.GOAL + "\n\n"
    "You are the Spec-Writer. Given the project brief and the user's answers, produce a "
    "complete, internally consistent software specification as JSON (ProjectSpec). Fill: "
    "goal (one clear sentence), non_goals, users, features, entities (data model with "
    "fields), backend_modules, backend_endpoints (method/path/purpose), frontend_screens, "
    "frontend_state, tech, scale, hard_rules, security, phases (each with concrete tasks), "
    "and assumptions (derived from the answers). Be concrete and consistent with the "
    "answers. Do not invent requirements the user rejected. Return ONLY the JSON object."
)


def _compact(brief: ProjectBrief, qa: list[tuple[str, str]], feedback: str) -> str:
    lines = [
        f"title: {brief.title}",
        f"type: {brief.project_type}",
        f"summary: {brief.summary}",
        f"known_features: {'; '.join(brief.features) or 'none'}",
        f"known_users: {', '.join(brief.users) or 'unknown'}",
        f"known_tech: {', '.join(brief.tech) or 'unknown'}",
        "answers:",
    ]
    lines += [f"- {q}: {a}" for q, a in qa if a.strip()]
    if feedback.strip():
        lines.append(f"requested_changes: {feedback.strip()[:500]}")
    return "\n".join(lines)


async def run_planner(
    brief: ProjectBrief,
    qa: list[tuple[str, str]],
    feedback: str = "",
) -> ProjectSpec:
    fallback = specgen.deterministic_spec(brief, qa, feedback)
    if not get_settings().has_llm:
        return fallback
    try:
        out = await runtime.run_structured(
            _SYS, _compact(brief, qa, feedback), ProjectSpec, SPEC_MAX_OUTPUT_TOKENS
        )
    except Exception:
        out = None
    return specgen.normalize_spec(out, fallback) if out else fallback
