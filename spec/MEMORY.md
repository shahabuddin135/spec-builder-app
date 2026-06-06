# MEMORY — Decisions & Assumptions

Frozen facts. If anything conflicts, this file wins.

## Decisions

- **Product:** SpecForge is a **spec generator + reviewer**. Vague brief → parse →
  clarifying questions → review/correct → downloadable `specs.zip`. (Pivoted from an
  earlier marketing-strategy prototype; that domain and its files were removed.)
- **No methodology jargon** in the product UI or generated output. The output follows the
  recommended folder structure (`SPEC.md`, `CONTEXT.md`, `backend_specs/`, …) as plain markdown.
- **No authentication** (prototype). Security rests on upload validation, untrusted-data
  framing, CORS lockdown, and rate limiting.
- **Deterministic-first agents:** every agent returns a valid result with no LLM, then tries
  the model and uses it only on success. Failure/timeout → deterministic result. No retries.
- **Tolerant LLM schemas:** agent output models carry no enums/range/length limits (providers
  reject their own output otherwise — e.g. a boolean field returned as a number); we normalize
  in app code.
- **Model routing:** Groq primary, OpenAI fallback, via LiteLLM. SDK imported lazily so the
  app runs without `openai-agents`/`litellm` installed.
- **DB:** Neon Postgres in prod; falls back to local SQLite (`aiosqlite`) when `DATABASE_URL`
  is unset. JSONB on Postgres via variant, JSON on SQLite.
- **Run command:** `uvicorn backend.main:app` from the repo root (backend is a package, so
  `backend/agents/` doesn't shadow the SDK's top-level `agents`).
- **Deploy Python = 3.12** (`.python-version` / `render.yaml`). litellm requires
  `>=3.10,<3.14`; Render's default 3.14 has no matching wheels.

## Assumptions

- Generated specs follow the small-project rule: single-file ARCH/PLAN/CONTRACT per side.
- Clarifying questions are AI-generated, with a deterministic default set as fallback.
- Spec review = free-text "request changes" → regenerate (capped at `MAX_SPEC_REVISIONS`).

## Do not change

- Raw brief is only sent to the Analyst, bounded (`BRIEF_INPUT_CHARS`) and wrapped as untrusted.
- 800-token agent input ceiling; outputs small except the spec object (`SPEC_MAX_OUTPUT_TOKENS`).
- Upload limit 256 KB; `.txt`/`.md` only; UUID storage names.
- UI transitions are driven by `/events`, never POST returns.

## Operational note

The `analyses`/`specs` schema changed during the pivot. `create_all` does **not** alter
existing tables — if reusing an old Neon database, drop the old tables first (or use a fresh DB).
