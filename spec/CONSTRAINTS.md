# CONSTRAINTS — Hard Limits

These override plans and tasks.

## Tech

- **Backend:** FastAPI, Python **3.12** (deploy on Render). SQLAlchemy 2.0 async; Neon
  Postgres (`sslmode=require`) or local SQLite fallback.
- **Agents:** OpenAI Agents SDK via LiteLLM — Groq primary, OpenAI fallback. SDK imported lazily.
- **Frontend:** Next.js (App Router, TS) + Tailwind v4 on Vercel; consumes the SSE stream.
- **Files:** uploads are `.txt` / `.md`, UTF-8, ≤256 KB. No PDF/docx/parsing.

## Scale

- Single-user prototype demo. Per-IP rate limits on cost-bearing routes.

## Hard rules

- 800-token agent input ceiling; the raw brief reaches only the Analyst, bounded and wrapped
  as untrusted data.
- Deterministic-first: the whole flow works with no model key; LLM enriches when present.
- One model call per agent step; no retry loops; per-call timeout.
- No authentication. No feature outside `CONTEXT.md` without updating it first.
- No methodology jargon in the product or generated output.
