# Backend Plan

Phases for the SpecForge backend. The deterministic path is first-class: the whole flow
works with no model key; the LLM enriches when a key is present.

### Phase 1 — Foundation (done)
Config, async DB (Neon or local SQLite), models (documents/analyses/specs), upload
validation + security, deterministic brief parser, SSE event bus.

### Phase 2 — Agent network (done)
`runtime.py` (LiteLLM → Groq/OpenAI, token ceiling, timeout), Analyst (parse),
Clarifier (questions), Planner/Spec-Writer (enriched spec), all with deterministic fallback.

### Phase 3 — Spec package + review (done)
`specgen.py` renders the full markdown tree and builds `specs.zip`; routes for analyze,
generate-specs, refine (request changes), and downloads.

### Phase 4 — Deploy (in progress)
Render web service; Python pinned to 3.12 (`render.yaml` / `.python-version`); CORS locked
to the Vercel origin; Neon `sslmode=require`.
