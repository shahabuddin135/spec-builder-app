# Backend Setup Guide — Marketing Strategy Spec Generator

FastAPI backend that runs a 3-agent network (Analyst → Strategist → Spec-Writer) over an
uploaded `.txt`/`.md` file and streams events to the frontend. **No authentication** (PoC):
security rests on upload validation, prompt-injection framing, CORS lockdown, and rate limiting.

This guide gets the **full backend flow** running (upload → analyze → suggestions → refine →
specs). It runs with **zero config** on the deterministic path (no LLM, no Neon); add API keys
to switch the agents on. The agent layer always falls back to the deterministic path on any
error/timeout, so the flow never hangs. See [spec/backend_specs/PLAN.md](../spec/backend_specs/PLAN.md).

---

## 1. Prerequisites

- **Python 3.11** is the spec target ([CONSTRAINTS.md](../spec/CONSTRAINTS.md)). 3.12/3.13 also work
  for local dev; pin 3.11 on Render for the deploy.
- A terminal at the **repo root** (`spec-builder-app/`). The backend runs as a package
  (`backend.main:app`), so commands run from the root, not from inside `backend/`.
- Optional: a [Neon](https://neon.tech) Postgres database. Without one, the app uses a local
  SQLite file automatically.
- Optional: Groq and/or OpenAI API keys. Without them, the deterministic fallback path runs.

---

## 2. Install

```powershell
# from the repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1            # Windows PowerShell
# source .venv/bin/activate             # macOS/Linux

pip install -r backend/requirements.txt
```

> Phase 1 only needs a subset; the full `requirements.txt` also installs the Phase 3 agent
> stack (`litellm`, `openai-agents`). All versions are pinned and were verified on PyPI.

---

## 3. Configure environment

```powershell
Copy-Item backend/.env.example backend/.env   # then edit backend/.env
```

Canonical env vars (**never invent new names** — [MEMORY.md](../spec/MEMORY.md)):

| Var | Required? | Purpose |
|-----|-----------|---------|
| `DATABASE_URL` | optional | Neon Postgres URL (`...?sslmode=require`). Unset → local SQLite. |
| `GROQ_API_KEY` | optional | Primary model (fast/cheap). Unset → deterministic fallback. |
| `OPENAI_API_KEY` | optional | Fallback model for the structured/critical step. |
| `LLM_API_KEY` | optional | Generic gateway key if used. |
| `ALLOWED_ORIGIN` | yes (prod) | Exact frontend origin for CORS. Never `*`. |
| `RATE_LIMIT` | optional | Per-IP limit, e.g. `20/minute`. |

`.env` is git-ignored. **No secret ever reaches the browser** — all model calls are server-side.

---

## 4. Run

```powershell
uvicorn backend.main:app --reload --port 8000
```

On startup the app creates tables (`create_all`, no migrations). Check it's alive:

```powershell
curl http://localhost:8000/health
# {"status":"ok","llm_enabled":false}
```

`llm_enabled` reflects whether any model key is set — `false` means the deterministic path is active.

---

## 5. Walk the full flow (curl)

The UI is meant to drive this off the `/events` SSE stream; here's the raw API order. Open a
second terminal and run `curl.exe -N http://localhost:8000/events` to watch the named events
(`analysis.started`, `analysis.done`, `suggestions.ready`, `spec.generated`) as you go.

```powershell
# 1) Upload -> {"document_id": "..."}   (.pdf -> 415, >256KB -> 413, binary -> 422)
"save 30% today, loyal members earn reward points. brand tone: playful" | Out-File -Encoding utf8 sample.txt
curl.exe -F "file=@sample.txt;type=text/plain" http://localhost:8000/upload

# 2) Analyze -> {"analysis_id": "..."}   (runs Analyst->Strategist in the background; watch /events)
curl.exe -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d "{\"document_id\":\"<DOC_ID>\"}"

# 3) Feedback (self-learning) -> 204
curl.exe -X POST http://localhost:8000/feedback -H "Content-Type: application/json" -d "{\"strategy_id\":\"loyalty\",\"action\":\"approve\"}"

# 4) Refine (bounded to 3, then 409) -> emits suggestions.ready
curl.exe -X POST http://localhost:8000/refine -H "Content-Type: application/json" -d "{\"analysis_id\":\"<ANALYSIS_ID>\",\"feedback\":\"focus on loyalty\"}"

# 5) Generate specs -> {"spec_id","files":[...]} ; emits spec.generated
curl.exe -X POST http://localhost:8000/generate-specs -H "Content-Type: application/json" -d "{\"analysis_id\":\"<ANALYSIS_ID>\",\"approved_ids\":[\"loyalty\"]}"

# 6) Download a generated file (attachment, sanitized name)
curl.exe -OJ http://localhost:8000/specs/<SPEC_ID>/marketing-strategy-spec.md
```

Acceptance criteria: [requirements.md](../requirements.md) §12. With no model key the whole flow
still works (deterministic fallback); the token-ceiling assert fires if an agent prompt is bloated.

### Test the requirements (acceptance check)

A repeatable check maps the live app to [requirements.md](../requirements.md) §12 using the
example uploads in [examples/](../examples/). Run it from the repo root (isolated: forces local
SQLite, clears keys, never touches Neon):

```powershell
$env:DATABASE_URL=""; $env:GROQ_API_KEY=""; $env:OPENAI_API_KEY=""; $env:LLM_API_KEY=""
.venv\Scripts\python.exe acceptance_check.py        # -> 13/13 acceptance checks PASSED
```

Covers: upload→FeatureCard, .pdf/oversize/binary rejection, event-driven flow, two uploads →
different on-brand suggestions, restricted-keyword guardrails, prompt-injection ignored, refine
(bounded), self-learning re-rank, downloadable specs, deterministic fallback, token ceiling, CORS.

### Enable the agents (optional)

Set `GROQ_API_KEY` (primary) and/or `OPENAI_API_KEY` (fallback) in `backend/.env`, then restart.
`GET /health` reports `"llm_enabled": true`. Routing is Groq → OpenAI via LiteLLM; each agent
call is capped at `max_tokens=256`, a 30s timeout, and the 800-token input ceiling — on any
failure it falls back to the deterministic result.

---

## 6. Project layout (backend)

```
backend/
├── main.py          # FastAPI app, CORS, /upload, /health  (routers grow in Phase 2)
├── config.py        # env settings, token budgets, constants
├── db.py            # async engine/session; Neon OR local SQLite; create_all
├── models_db.py     # SQLAlchemy 2.0 models (5 tables)
├── schemas.py       # pydantic request/response + agent I/O
├── security.py      # upload validation, safe naming, rate limiter   (P0 controls)
├── ingest.py        # deterministic text -> FeatureCard (NO LLM)
├── strategies.py    # fixed library of 7 + enum source of truth
├── seed/strategies.json
├── agents/          # Phase 3: runtime, analyst, strategist, specwriter, guardrails
├── events.py        # Phase 2: SSE event bus
├── learning.py      # Phase 4: strategy_stats bias
├── specgen.py       # Phase 2/3: assemble downloadable spec files
└── requirements.txt
```

---

## 7. Context7 MCP (docs source for this build)

`.mcp.json` (repo root) registers the **Context7** MCP server so the assistant fetches
current docs (FastAPI, SQLAlchemy 2.0 async, LiteLLM, OpenAI Agents SDK, slowapi) before
implementing any integration. Approve it once when prompted (or via `/mcp`). No API key is
required for the free tier.

---

## 8. Security checklist (do not skip — [SECURITY.md](../spec/SECURITY.md))

- Uploads: `.txt`/`.md` + content-type allowlist, 256 KB cap, UTF-8/null-byte reject, UUID storage.
- SQLAlchemy parameterized queries only — never string-built SQL.
- Secrets in env vars only; `.env` git-ignored; no key in the client bundle.
- CORS locked to `ALLOWED_ORIGIN`; rate limit on cost-bearing endpoints.
- Uploaded text is treated as untrusted DATA, never as instructions (prompt-injection defense).
- Model output is always parsed/validated before use — it can never run SQL, write files, or call endpoints.

---

## 9. Deploy (Render) — Phase 5

- Push repo; create a Render Web Service, root = repo root.
- Build: `pip install -r backend/requirements.txt`
- Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- Set env vars in Render's secret store; set `ALLOWED_ORIGIN` to the exact Vercel URL.
- Use a Neon `DATABASE_URL` with `sslmode=require`. HTTPS is automatic.
- If time is short, demo locally — local + the security controls beats a half-broken deploy.
