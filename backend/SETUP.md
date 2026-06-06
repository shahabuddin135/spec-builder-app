# Backend Setup — SpecForge (Spec Generator)

FastAPI backend that turns a project brief into a reviewed spec package and a downloadable
`specs.zip`. Runs with **zero config** on the deterministic path (no LLM, no Neon); add a
`GROQ_API_KEY` to switch the agents on. **No authentication** (prototype).

Flow: `upload brief → analyze (parse + clarifying questions) → answer → generate-specs →
review / request changes → download specs.zip`.

## 1. Prerequisites

- **Python 3.12** (recommended). `litellm` requires `>=3.10,<3.14`, so avoid 3.14.
- A terminal at the **repo root**. The backend runs as a package (`backend.main:app`).
- Optional: a [Neon](https://neon.tech) `DATABASE_URL` (else local SQLite is used) and a
  `GROQ_API_KEY` / `OPENAI_API_KEY` (else the deterministic path runs).

## 2. Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1            # Windows
# source .venv/bin/activate             # macOS/Linux
pip install -r backend/requirements.txt
```

## 3. Configure

```powershell
Copy-Item backend/.env.example backend/.env   # then edit
```

| Var | Required? | Purpose |
|-----|-----------|---------|
| `DATABASE_URL` | optional | Neon URL (`...?sslmode=require`). Unset → local SQLite. |
| `GROQ_API_KEY` | optional | Primary model. Unset → deterministic fallback. |
| `OPENAI_API_KEY` | optional | Fallback model. |
| `ALLOWED_ORIGIN` | yes (prod) | Exact frontend origin for CORS. Never `*`. |
| `RATE_LIMIT` | optional | Per-IP limit, e.g. `20/minute`. |

## 4. Run

```powershell
uvicorn backend.main:app --reload --port 8000     # from the repo root
curl http://localhost:8000/health                  # {"status":"ok","llm_enabled":...}
```

## 5. Walk the flow (curl)

Open a second terminal: `curl.exe -N http://localhost:8000/events` to watch the events.

```powershell
"# Habit Tracker`nA web app to track daily habits and streaks." | Out-File -Encoding utf8 brief.md
curl.exe -F "file=@brief.md;type=text/markdown" http://localhost:8000/upload          # -> {document_id}
curl.exe -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d "{\"document_id\":\"<DOC>\"}"
# watch /events for questions.ready, then:
curl.exe -X POST http://localhost:8000/generate-specs -H "Content-Type: application/json" -d "{\"analysis_id\":\"<AID>\",\"answers\":[]}"
curl.exe -OJ http://localhost:8000/specs/<SPEC_ID>/archive.zip                          # -> specs.zip
```

## 6. Test the requirements

```powershell
$env:DATABASE_URL=""; $env:GROQ_API_KEY=""; $env:OPENAI_API_KEY=""; $env:LLM_API_KEY=""
.venv\Scripts\python.exe acceptance_check.py        # -> 10/10 acceptance checks PASSED
```

Isolated: forces local SQLite, clears keys, never touches Neon. Uses the briefs in `examples/`.

## 7. Deploy (Render)

- `render.yaml` is included: build `pip install -r backend/requirements.txt`, start
  `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.
- **Pin Python to 3.12** — set `PYTHON_VERSION=3.12.8` (or rely on `.python-version`). The
  default 3.14 has no `litellm`/`asyncpg` wheels and the build fails.
- Set env vars in Render's secret store; set `ALLOWED_ORIGIN` to the exact Vercel URL.
- Use a Neon `DATABASE_URL` with `sslmode=require`.
- **Schema note:** the data model changed during the pivot. `create_all` does not alter
  existing tables — if reusing an old Neon DB, drop the old tables (or use a fresh one).

## 8. Security (prototype, no auth)

Upload allowlist + 256 KB cap + UTF-8/null-byte checks + UUID storage; parameterized SQL
only; secrets server-side; CORS locked to `ALLOWED_ORIGIN`; rate limits on cost-bearing
routes; the brief is treated as untrusted data and model output is always validated before use.
