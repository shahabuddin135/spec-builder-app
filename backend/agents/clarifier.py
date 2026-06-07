"""Clarifier: ProjectBrief -> clarifying questions to ask the user.

LLM generates questions tailored to what's vague; the deterministic fallback asks
a sensible default set keyed off the brief's open_areas.
"""
from __future__ import annotations

from backend.agents import runtime
from backend.config import QUESTIONS_MAX_OUTPUT_TOKENS, get_settings
from backend.schemas import ProjectBrief, Question, QuestionsOut

_SYS = (
    runtime.GOAL + "\n\n"
    "You are the Clarifier. Given the parsed project brief (JSON), produce 3 to 6 short, "
    "high-impact clarifying questions that resolve the most important ambiguities about "
    "what the user wants to build. Each question has: id (slug), question, why (one line), "
    "and up to 4 suggestions. Ask about target users, must-have v1 features, data/storage, "
    "tech/hosting, and what is out of scope — only where the brief is unclear. "
    "Return ONLY the JSON object {\"questions\": [...]}."
)


def _q(qid: str, question: str, why: str, suggestions: list[str]) -> Question:
    return Question(id=qid, question=question, why=why, suggestions=suggestions)


def default_questions(brief: ProjectBrief) -> list[Question]:
    qs: list[Question] = []
    if not brief.goals:
        qs.append(
            _q("goal", "What is the single most important outcome this should achieve?",
               "Anchors the whole spec.", [])
        )
    if not brief.users:
        qs.append(
            _q("users", "Who are the primary users of this product?",
               "Access rules and screens depend on who uses it.",
               ["End consumers", "Internal team", "Businesses (B2B)", "Admins + members"])
        )
    qs.append(
        _q("features", "What are the 3–5 must-have features for the first version?",
           "Keeps v1 scope focused.", [])
    )
    qs.append(
        _q("data", "What data does the app store, and where?",
           "Drives the data model and storage choice.",
           ["Relational DB", "Files only", "External API", "No persistence"])
    )
    if not brief.tech:
        qs.append(
            _q("tech", "Any preferred tech stack or hosting?",
               "Pins the constraints.",
               ["Next.js + FastAPI", "Whatever you recommend", "Must reuse existing stack"])
        )
    qs.append(
        _q("scope", "What is explicitly out of scope for v1?",
           "Prevents scope creep.",
           ["Auth/accounts", "Payments", "Mobile app", "Admin tools"])
    )
    return qs[:6]


def _compact(brief: ProjectBrief) -> str:
    return (
        f"title: {brief.title}\n"
        f"type: {brief.project_type}\n"
        f"summary: {brief.summary}\n"
        f"known_features: {'; '.join(brief.features) or 'none'}\n"
        f"known_users: {', '.join(brief.users) or 'unknown'}\n"
        f"known_tech: {', '.join(brief.tech) or 'unknown'}\n"
        f"open_areas: {', '.join(brief.open_areas) or 'none'}"
    )


def _normalize(questions: list[Question]) -> list[Question]:
    out: list[Question] = []
    for i, q in enumerate(questions[:6], 1):
        if not q.question.strip():
            continue
        out.append(
            Question(
                id=q.id.strip() or f"q{i}",
                question=q.question.strip(),
                why=q.why.strip(),
                suggestions=[s for s in q.suggestions if s][:4],
            )
        )
    return out


async def run_clarifier(brief: ProjectBrief) -> list[Question]:
    fallback = default_questions(brief)
    if not get_settings().has_llm:
        return fallback
    try:
        out = await runtime.run_structured(
            _SYS, _compact(brief), QuestionsOut, QUESTIONS_MAX_OUTPUT_TOKENS
        )
    except Exception:
        out = None
    if not out or not out.questions:
        return fallback
    return _normalize(out.questions) or fallback
