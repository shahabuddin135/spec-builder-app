# Task Index

Single source of truth for task status.

| ID | Task | Status |
|----|------|--------|
| 1.1 | Config, async DB (Neon/SQLite), models | done |
| 1.2 | Upload validation + security (size, type, UUID storage) | done |
| 1.3 | Deterministic brief parser (`ingest.py`) | done |
| 1.4 | SSE event bus (`events.py`) | done |
| 2.1 | `runtime.py` — LiteLLM routing, token ceiling, timeout | done |
| 2.2 | Analyst — brief → ProjectBrief (+fallback) | done |
| 2.3 | Clarifier — brief → clarifying questions (+fallback) | done |
| 2.4 | Planner/Spec-Writer — brief+answers → ProjectSpec (+fallback) | done |
| 3.1 | `specgen.py` — render full markdown tree | done |
| 3.2 | `build_zip` — bundle specs.zip | done |
| 3.3 | Routes: analyze, generate-specs, refine | done |
| 3.4 | Downloads: archive.zip + single file | done |
| 3.5 | Acceptance check (examples → flow → zip) | done |
| 4.1 | Render deploy (Python 3.12 pin, CORS, Neon) | todo |
