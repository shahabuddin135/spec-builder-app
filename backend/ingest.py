"""Deterministic brief -> ProjectBrief (NO LLM).

Heuristic parse that always produces a usable structured brief. It is the
fallback for the Analyst agent and keeps the whole flow working with no model key.
Pure functions: same input always yields the same output.
"""
from __future__ import annotations

import re

from backend.schemas import ProjectBrief

_BULLET = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.*\S)\s*$")
_HEADING = re.compile(r"^\s*#{1,6}\s+(.*\S)\s*$")

_TYPE_CUES = [
    (("cli", "command line", "command-line", "terminal tool"), "cli"),
    (("rest api", "api service", "backend api", "graphql", "endpoint"), "api"),
    (("mobile", "ios", "android", "react native", "flutter"), "mobile"),
    (("dashboard", "web app", "webapp", "website", "saas", "portal", "platform"), "web app"),
]

_TECH = [
    "react", "next.js", "nextjs", "next", "vue", "svelte", "angular", "remix",
    "fastapi", "flask", "django", "express", "node", "nestjs", "rails",
    "python", "typescript", "javascript", "go", "rust", "java", "kotlin",
    "postgres", "postgresql", "mysql", "sqlite", "mongodb", "redis", "supabase",
    "tailwind", "graphql", "stripe", "auth0", "firebase",
]

_USER_WORDS = [
    "users", "customers", "admins", "administrators", "students", "teachers",
    "managers", "teams", "members", "patients", "clients", "sellers", "buyers",
    "creators", "developers", "guests", "owners", "staff", "subscribers",
]

_FEATURE_HINTS = ("should", "can ", "able to", "allow", "support", "let users", "be able")
_GOAL_HINTS = ("goal", "objective", "purpose", "aim", "want to", "help ", "so that")
_NONGOAL_HINTS = ("out of scope", "not ", "won't", "wont", "no need", "exclude", "later")


def _lines(text: str) -> list[str]:
    return [ln.rstrip() for ln in text.splitlines()]


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def _title(text: str) -> str:
    for ln in _lines(text):
        m = _HEADING.match(ln)
        if m:
            return m.group(1)[:80]
    for ln in _lines(text):
        if ln.strip():
            return ln.strip()[:80]
    return "Untitled Project"


def _summary(text: str) -> str:
    body = "\n".join(ln for ln in _lines(text) if not _HEADING.match(ln)).strip()
    sents = _sentences(body)
    return " ".join(sents[:2])[:300] if sents else body[:300]


def _bullets(text: str) -> list[str]:
    return [m.group(1) for ln in _lines(text) if (m := _BULLET.match(ln))]


def _dedupe(items: list[str], cap: int) -> list[str]:
    seen: list[str] = []
    for it in items:
        norm = it.strip()
        if norm and norm.lower() not in {s.lower() for s in seen}:
            seen.append(norm)
        if len(seen) >= cap:
            break
    return seen


def build_project_brief(text: str) -> ProjectBrief:
    low = text.lower()
    bullets = _bullets(text)
    sents = _sentences(text)

    project_type = "web app"
    for cues, label in _TYPE_CUES:
        if any(c in low for c in cues):
            project_type = label
            break

    features = _dedupe(
        bullets or [s for s in sents if any(h in s.lower() for h in _FEATURE_HINTS)],
        8,
    )
    goals = _dedupe([s for s in sents if any(h in s.lower() for h in _GOAL_HINTS)], 4)
    non_goals = _dedupe([s for s in sents if any(h in s.lower() for h in _NONGOAL_HINTS)], 4)
    users = _dedupe([w.capitalize() for w in _USER_WORDS if w in low], 6)
    tech = _dedupe([t for t in _TECH if t in low], 8)

    open_areas: list[str] = []
    if not users:
        open_areas.append("target users / audience")
    if not features:
        open_areas.append("must-have features for v1")
    if not tech:
        open_areas.append("preferred tech stack")
    open_areas += ["data & storage", "explicit out-of-scope for v1"]

    return ProjectBrief(
        title=_title(text),
        summary=_summary(text) or "A software project.",
        project_type=project_type,
        goals=goals or ([sents[0]] if sents else []),
        non_goals=non_goals,
        users=users,
        features=features,
        tech=tech,
        open_areas=_dedupe(open_areas, 6),
    )
