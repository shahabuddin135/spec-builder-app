# CONSTRAINTS.md — Reality Anchor

> Hard limits. These override all plans and tasks. Derived from `requirements.md` §1, §7, §9.

## TECH

- **Backend:** FastAPI, Python 3.11 (deploy target: Render, HTTPS auto).
- **DB:** Neon Postgres via SQLAlchemy 2.0 **async**; `sslmode=require`. May degrade to an
  in-memory dict if Neon fights the timebox.
- **Agents:** OpenAI Agents SDK (Python) — orchestration, structured outputs, guardrails.
- **Model gateway:** LiteLLM single gateway. Primary: **Groq** (fast/cheap Llama-3.x).
  Fallback: **OpenAI** (small GPT-4-class) for the structured/critical step.
- **Frontend:** Next.js (App Router, TS) on Vercel; Vercel AI SDK as streaming/UI layer only.
- **Files:** `.txt` / `.md` only, UTF-8 plain text. No PDF/docx/parsing/OCR.
- Verify LiteLLM↔Agents-SDK import paths and Vercel AI SDK stream helpers against
  **current docs via Context7 MCP** — do not assume.

## SCALE

- Single-brand, single-user demo. No concurrency targets beyond a demo.
- Per-IP rate limits on `/analyze` and `/generate-specs` (e.g. slowapi).
- Upload max size: **256 KB**.

## HARD RULES (non-negotiable)

- **Token ceiling:** `MAX_AGENT_INPUT_TOKENS = 800`; `runtime.py` estimates (`len//4`) and
  **raises** if exceeded. Outputs small JSON, `max_tokens ≤ 256`.
- Agents never receive raw upload text after the Analyst step — only the compact
  `FeatureCard` (~40 tokens) flows downstream. Raw `content` is never sent to an LLM.
- Brand card + strategy library passed as compact `id:desc` lines, never prose.
- Learning passed as **aggregates only** (`strategy_stats` top-3), never event logs.
- One call per agent per step. No chains in the request path. No autonomous looping.
- Cache analysis by `sha256(content)` — identical upload never re-runs.
- Refine loop bounded to **3 iterations**.
- `strategy_id` enum-constrained to the live library; invalid id → drop the item.
- **Priority to keep if timeboxed:** FastAPI + Agents + LiteLLM/Groq + deterministic
  fallback. Neon may degrade to in-memory; deploy may degrade to local.
  **Never cut the security controls in SECURITY.md.**
- Canonical env vars only (never invent names):
  `DATABASE_URL`, `LLM_API_KEY` / `GROQ_API_KEY` / `OPENAI_API_KEY`, `ALLOWED_ORIGIN`, `RATE_LIMIT`.
