# tasks/task_index.md — Global Task Registry (HOT)

> Single source of truth for task status. All tasks visible from the start (not locked).
> LLM reads this once, then loads only the individual task file it needs.
> Phase-1 task files exist now; phases 2–5 files are generated just-in-time when the
> phase begins (consistent with the project's load-only-what-you-need budget).

```slc
@block INDEX task_registry
priority: critical
intent: "Global backend task registry — all tasks visible"
scope: global
failure_if_skipped: true

content:
  total_tasks: 28

  phases:
    - phase: 1
      name: "Foundation (NO LLM)"
      dir: "phases/phase-1/"
      tasks: 9
    - phase: 2
      name: "Routes + SSE + deterministic Strategist"
      dir: "phases/phase-2/"
      tasks: 8
    - phase: 3
      name: "Agent network (LLM path)"
      dir: "phases/phase-3/"
      tasks: 7
    - phase: 4
      name: "Learning + refine"
      dir: "phases/phase-4/"
      tasks: 4
    - phase: 5
      name: "Deploy + hardening"
      dir: "phases/phase-5/"
      tasks: 0   # tasks enumerated when phase begins

  all_tasks:
    # Phase 1 — Foundation  (DONE — verified via §12.1 smoke 2026-06-06)
    - { id: "1.1", file: "phases/phase-1/1.1_init_project.md",     status: done }
    - { id: "1.2", file: "phases/phase-1/1.2_config.md",           status: done }
    - { id: "1.3", file: "phases/phase-1/1.3_db.md",               status: done }
    - { id: "1.4", file: "phases/phase-1/1.4_models_db.md",        status: done }
    - { id: "1.5", file: "phases/phase-1/1.5_schemas.md",          status: done }
    - { id: "1.6", file: "phases/phase-1/1.6_security.md",         status: done }
    - { id: "1.7", file: "phases/phase-1/1.7_ingest.md",           status: done }
    - { id: "1.8", file: "phases/phase-1/1.8_strategies_seed.md",  status: done }
    - { id: "1.9", file: "phases/phase-1/1.9_verify_foundation.md",status: done }
    # Phase 2 — Routes + SSE + deterministic Strategist  (DONE — e2e smoke 2026-06-06)
    - { id: "2.1", desc: "events.py asyncio broadcast -> SSE generator",        status: done }
    - { id: "2.2", desc: "POST /upload route (uses security.py)",               status: done }
    - { id: "2.3", desc: "POST /analyze route (background pipeline, sha cache)", status: done }
    - { id: "2.4", desc: "deterministic Strategist (rank by scorer)",           status: done }
    - { id: "2.5", desc: "specgen.py assemble + redact spec files",             status: done }
    - { id: "2.6", desc: "POST /generate-specs + GET /specs/{id}/{name}",       status: done }
    - { id: "2.7", desc: "main.py wiring: CORS, routers, exception handlers",   status: done }
    - { id: "2.8", desc: "verify full flow with NO LLM key (e2e smoke)",        status: done }
    # Phase 3 — Agent network  (DONE — fallback + token assert verified; live LLM needs keys)
    - { id: "3.1", desc: "runtime.py LiteLLM config + token-ceiling + timeout",  status: done }
    - { id: "3.2", desc: "analyst.py (bounded excerpt) -> FeatureCard+brand_card",status: done }
    - { id: "3.3", desc: "strategist.py (LLM, enum-constrained) + fallback",     status: done }
    - { id: "3.4", desc: "specwriter.py -> 3 spec files (LLM md + fallback)",     status: done }
    - { id: "3.5", desc: "guardrails.py keyword/length + safe template + redact", status: done }
    - { id: "3.6", desc: "Groq primary + OpenAI fallback wiring",                status: done }
    - { id: "3.7", desc: "verify fallback + token assert (no-key path)",         status: done }
    # Phase 4 — Learning + refine  (DONE — re-rank verified)
    - { id: "4.1", desc: "learning.py record + read top-3 stats bias",          status: done }
    - { id: "4.2", desc: "POST /feedback route -> strategy_stats (204)",        status: done }
    - { id: "4.3", desc: "POST /refine route (bounded 3 -> 409)",               status: done }
    - { id: "4.4", desc: "verify self-learning re-ranks on re-run",             status: done }
@end
```
