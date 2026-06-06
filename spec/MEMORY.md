# MEMORY.md — Anti-Hallucination Anchor

> Frozen facts and decisions. If a conflict arises, MEMORY.md wins (below SPEC + requirements.md).
> Role placeholders only — never real names.

## DECISIONS

- 2026-06-06 — {USER} confirmed: **no authentication** in this prototype. Auth is a NON-GOAL.
  Security rests on upload validation, prompt-injection framing, CORS lockdown, and rate limiting.
- 2026-06-06 — **Context7 MCP added** at project scope (`.mcp.json`, HTTP transport,
  `https://mcp.context7.com/mcp`, no API key — free tier). Used to fetch current docs before
  implementing any framework/library integration. Server is "pending approval" until {USER} trusts it.
- SLC layout: specs live in `spec/`; runnable code lives in `backend/` and `frontend/`
  (per requirements.md §3). Single-file mode chosen for ARCH/PLAN/CONTRACT (small project,
  <4KB, ≤10 endpoints) — no split directories.
- Model routing: Groq primary, OpenAI fallback, via LiteLLM gateway.
- Deterministic fallback path is first-class: the full flow must work with the LLM key removed.
- 2026-06-06 — Backend runs as a **Python package**: `uvicorn backend.main:app` from the repo
  root, imports are absolute (`backend.*`). Reason: the spec's `backend/agents/` directory
  would otherwise shadow the OpenAI Agents SDK's top-level `agents` package. Keeps §3's name.
- 2026-06-06 — **DB degrade path = local SQLite via `aiosqlite`** (not a raw in-memory dict).
  Reason: one SQLAlchemy code path for both targets (uniform parameterized queries); JSON
  columns are JSONB on Postgres via `with_variant`, plain JSON on SQLite. `aiosqlite` added
  to requirements.txt (not in requirements.md §3 list — recorded deviation, degrade path only).
- 2026-06-06 — **Analyst sees a bounded excerpt** (`ANALYST_INPUT_CHARS=1800`, ~≤800 tokens),
  wrapped as untrusted `<<<DATA…DATA>>>`. Resolves the tension between §6 (Analyst reads the
  upload) and §7.4 (800-token ceiling). The deterministic `ingest` reads the FULL text for the
  fallback FeatureCard. Verified: `assert_within_budget` raises on bloat.
- 2026-06-06 — **Deterministic-first agent layer.** Every agent (`run_analyst/strategist/
  specwriter`) computes a deterministic result, then tries the LLM and returns it only on
  success; ANY failure (no key, SDK missing, API error, bad output, or a 30s `LLM_TIMEOUT_SECONDS`
  timeout) returns the deterministic result. No retry loops, no hangs. SDK imported lazily so the
  package loads without `openai-agents`/`litellm`. LiteLLM model class confirmed via docs:
  `from agents.extensions.models.litellm_model import LitellmModel` (needs `openai-agents[litellm]`).
- 2026-06-06 — **/analyze is event-driven**: it returns `{analysis_id}` immediately and runs the
  Analyst→Strategist pipeline as a background asyncio task that publishes `analysis.started/done`
  and `suggestions.ready` to the SSE bus. UI advances on events, not the POST return.
- 2026-06-06 — **Tolerant LLM-facing schemas** (`AnalystLLMOut`, `StrategistLLMOut`, `MarkdownOut`
  in schemas.py). Live Groq returned `is_new` as a *number* (0.2), which a strict `bool` tool
  schema rejected (`tool_use_failed`) → Analyst always fell back. Fix: LLM schemas carry NO
  enum/range/length constraints; we clamp floats, threshold `is_new>=0.5`, drop invalid
  `strategy_id` (§8.1 "drop item"), and truncate fields in app code. Verified live: Analyst +
  Strategist both return real LLM output via Groq.
- 2026-06-06 — **Learning bias weight raised** to make §12.5 demoable: deterministic score =
  `0.45*target + 0.30*fit + 0.25*bias` (was 0.5/0.4/0.1). Verified: approve/reject moved
  `urgency` from rank 6 → 2.
- 2026-06-06 — **Requirements tested**: `acceptance_check.py` (repo root) drives the real ASGI app
  with `examples/acme_coffee_club.md` + `examples/aurora_skincare.md` → **13/13 §12 checks pass**
  on the deterministic path. Live Groq path confirmed separately (model `groq/llama-3.3-70b-versatile`
  valid; strategist ~20s cold, analyst ~1s).
- 2026-06-06 — {USER} created `backend/.env` with a real Neon `DATABASE_URL` and `GROQ_API_KEY`.
  `asyncpg` is NOT in the test `.venv` (Phase-1 subset only) → run `pip install -r backend/
  requirements.txt` to use Neon. The acceptance check forces SQLite + clears keys (env overrides
  `.env`) so it stays isolated, deterministic, and never writes to the real DB.

## ASSUMPTIONS

- Strategy library has exactly 7 fixed ids: `loyalty, discount, social, urgency, welcome, winback, novelty`.
- `discount` is seeded with a low `brand_fit` (~0.55).
- `feature_card` = `{persona, f:{price_sens,loyalty,recency,novelty,engage,is_new}, tags[<=4]}`
  is the ONLY user representation any agent sees.
- Spec-Writer outputs exactly three files: `marketing-strategy-spec.md`,
  `personalization-rules.json`, `brand-card.json`.
- LiteLLM↔Agents-SDK import path and Vercel AI SDK stream helpers are NOT assumed —
  verified via Context7 before use.

## DO NOT CHANGE

- `MAX_AGENT_INPUT_TOKENS = 800`; estimate via `len//4`; raise on exceed.
- Raw upload `content` is never sent to an LLM.
- Canonical env var names: `DATABASE_URL`, `LLM_API_KEY`/`GROQ_API_KEY`/`OPENAI_API_KEY`,
  `ALLOWED_ORIGIN`, `RATE_LIMIT`. Do not invent new env var names.
- Upload limit 256 KB; `.txt`/`.md` only; UUID storage names.
- Refine loop max 3 iterations.
- UI state transitions are driven by `/events`, never by POST return values.
