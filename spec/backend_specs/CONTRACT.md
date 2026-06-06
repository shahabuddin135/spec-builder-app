# API Contract

Base: FastAPI; CORS allows `ALLOWED_ORIGIN` only; no auth (prototype). JSON unless noted.
UI state transitions are driven by `/events`, not by POST return values.

## Endpoints

| Method | Path | Body | Returns / Emits |
|--------|------|------|-----------------|
| POST | `/upload` | multipart `.txt`/`.md`, ≤256 KB | `{document_id}` · 415 / 413 / 422 |
| POST | `/analyze` | `{document_id}` | `{analysis_id}` ; emits `analysis.started`, `analysis.done`, `questions.ready` |
| POST | `/generate-specs` | `{analysis_id, answers:[{id,answer}]}` | `{spec_id}` ; emits `spec.generating`, `spec.generated` |
| POST | `/refine` | `{analysis_id, feedback}` | `{spec_id}` ; emits `spec.generating`, `spec.generated` (revision++, capped) |
| GET | `/specs/{spec_id}/archive.zip` | — | `specs.zip` (attachment, `application/zip`) |
| GET | `/specs/{spec_id}/file/{path}` | — | one file (attachment, sanitized name) |
| GET | `/events` | — | `text/event-stream` (named events) |
| GET | `/health` | — | `{status, llm_enabled}` |

`/analyze`, `/generate-specs`, `/refine` are per-IP rate-limited (`RATE_LIMIT`).

## Event shape

`{type, ts, msg, data?}`

- `analysis.done` → `{analysis_id, title, project_type}`
- `questions.ready` → `{analysis_id, questions:[{id, question, why, suggestions[]}]}`
- `spec.generated` → `{spec_id, iteration, title, files:[{path, mime}]}`

## Generated package (in `specs.zip`)

`README.md`, `SPEC.md`, `CONTEXT.md`, `CONSTRAINTS.md`, `SECURITY.md`, `MEMORY.md`,
`backend_specs/{ARCH,CONTRACT,PLAN}.md`, `backend_specs/tasks/task_index.md`,
`frontend_specs/{ARCH,CONTRACT,PLAN}.md`, `frontend_specs/tasks/task_index.md`.
