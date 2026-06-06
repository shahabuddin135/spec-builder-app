# Backend Architecture

FastAPI (Python 3.12) + SQLAlchemy 2.0 async. Agent network via OpenAI Agents SDK,
routed through LiteLLM (Groq primary, OpenAI fallback). Event-driven over SSE.

## Data model

- **documents** — `id, safe_name, content, sha256, created_at`. The raw brief.
- **analyses** — `id, document_id, brief(jsonb), questions(jsonb), answers(jsonb), created_at`.
  `brief` is the parsed `ProjectBrief`; `questions` are the clarifying questions; `answers`
  are the user's responses.
- **specs** — `id, analysis_id, files(jsonb=[{path,mime,content}]), iteration, created_at`.
  The rendered package; `iteration` increments on each regenerate.

JSON columns are JSONB on Postgres, JSON on SQLite (one model, both targets).

## Agent network

1. **Analyst** (`agents/analyst.py`) — bounded, untrusted brief excerpt -> `ProjectBrief`.
2. **Clarifier** (`agents/clarifier.py`) — `ProjectBrief` -> 3-6 clarifying questions.
3. **Spec-Writer / Planner** (`agents/planner.py`) — brief + answers (+ change requests)
   -> enriched `ProjectSpec`. `specgen.py` renders it into the markdown file tree and
   builds `specs.zip`.

Every agent is **deterministic-first**: it computes a valid result with no LLM, then tries
the model and uses it only on success. Any failure (no key, SDK missing, API error, bad
output, or a timeout) returns the deterministic result — no retry loop, no hang.
`runtime.py` enforces an 800-token input ceiling and a per-call timeout.

## Flow & events

`upload -> analyze (parse + questions) -> generate-specs (answers -> package) ->
refine (request changes) -> download`.

`/analyze` and `/generate-specs` return an id immediately and run the pipeline as a
background task that publishes SSE events: `analysis.started`, `analysis.done`,
`questions.ready`, `spec.generating`, `spec.generated`, `error`. The UI transitions on
events, never on POST return values.

## Boundaries

- Routes never call models directly — they spawn pipelines that call the agents.
- Model output is always parsed/validated before use; it can never run SQL, write files,
  or trigger privileged actions.
- The raw brief is only ever sent to the Analyst, bounded and wrapped as untrusted data.
