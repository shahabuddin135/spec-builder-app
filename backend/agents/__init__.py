"""Agent network (Analyst -> Strategist -> Spec-Writer).

Submodules import the OpenAI Agents SDK lazily, inside guarded run functions, so
that the deterministic fallback path works even when the SDK is not installed or no
model key is set. This package is `backend.agents`; the SDK is top-level `agents`.
"""
