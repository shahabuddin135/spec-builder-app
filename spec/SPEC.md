# SPEC.md — Global Router (Entry Point)

> Single entry point for this SLC project. Read this file first, then follow the
> READ ORDER exactly. Source of truth for intent is `requirements.md` at repo root
> (the frozen BUILD PROMPT). These spec files derive from it — they never extend it.

```slc
@block INDEX root
priority: critical
intent: "Reading router for the Marketing Strategy Spec Generator PoC"
scope: global
failure_if_skipped: true

read_order:
  - CONTEXT.md
  - CONSTRAINTS.md
  - SECURITY.md
  - MEMORY.md
  - backend_specs/ARCH.md
  - backend_specs/CONTRACT.md
  - backend_specs/PLAN.md
  - backend_specs/tasks/task_index.md

must_read_latest:
  - service: "FastAPI"
    url_hint: "context7://fastapi"
  - service: "SQLAlchemy 2.0 (async)"
    url_hint: "context7://sqlalchemy"
  - service: "OpenAI Agents SDK (Python)"
    url_hint: "context7://openai-agents-python"
  - service: "LiteLLM"
    url_hint: "context7://litellm"
  - service: "slowapi"
    url_hint: "context7://slowapi"

content:
  short: "Follow read_order exactly. Specs derive from requirements.md; never invent."
@end
```

## EXECUTION RULES

- No code generation before ARCH + CONTRACT are finalized.
- `requirements.md` (root) is the frozen intent. `CONTRACT.md` is authoritative for the API.
- Build follows `PLAN.md` phase order; the deterministic fallback path is protected first.
- Before implementing any framework/library integration, call **Context7 MCP**
  (`resolve-library-id` → `get-library-docs`) per `must_read_latest`. Do not assume APIs.
- `tasks/task_index.md` is the single source of truth for task status.
- Violations must abort execution and be reported (do not silently correct).

## APPROVAL GATES

1. Specs (this dir) reviewed by `{USER}` before code is written.
2. `task_index.md` reviewed before execution begins.
3. Any change to CONTEXT / CONSTRAINTS / SECURITY requires re-validation and a MEMORY.md entry.

## FINAL AUTHORITY (conflict resolution)

`requirements.md` > SPEC.md > MEMORY.md > SECURITY.md > CONSTRAINTS.md > ARCH.md > PLAN.md > tasks.
