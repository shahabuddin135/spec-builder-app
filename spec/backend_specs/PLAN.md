# backend/PLAN.md — Execution Phases (single-file mode)

> 5 phases → single file. High-level phases only; no implementation detail.
> Derived from `requirements.md` §11 build order. **Protect the deterministic fallback path.**

```slc
@block PLAN backend_phases
priority: high
intent: "Backend phase plan, ordered. Each phase is demoable before the next begins."
scope: global
depends_on: [ARCH.data_model, CONTRACT.http_api]

content:
  total_phases: 5

  phases:
    - id: 1
      name: "Foundation (NO LLM)"
      summary: "Scaffold + config, db, models_db, schemas, security (upload validation),
                ingest (deterministic FeatureCard), strategies seed. Verify upload->FeatureCard by curl."
      gate: "curl uploads a .txt and gets a FeatureCard; a .pdf/2MB file is rejected (415/413)."

    - id: 2
      name: "Routes + SSE + deterministic Strategist"
      summary: "FastAPI routers, events.py broadcast/SSE, deterministic Strategist (rank by scorer).
                Whole flow works with ZERO LLM. specgen produces files from deterministic output."
      gate: "Full Upload->Analyze->Suggestions->Specs loop via curl, no LLM key set."

    - id: 3
      name: "Agent network (LLM path)"
      summary: "runtime.py (LiteLLM->Groq primary/OpenAI fallback + token ceiling), Analyst,
                Strategist, Spec-Writer, guardrails.py. Structured outputs; fallback on failure."
      gate: "Two uploads yield different on-brand suggestions; restricted keyword never appears;
             token-ceiling assert fires on bloated input; key removed -> deterministic path still works."

    - id: 4
      name: "Learning + refine"
      summary: "learning.py: approve/reject -> strategy_stats; Strategist reads top-3 as ranking bias.
                /refine bounded to 3 iterations."
      gate: "Approve/reject changes strategy_stats; a re-run visibly re-ranks (self-learning)."

    - id: 5
      name: "Deploy + hardening"
      summary: "Deploy backend->Render, set env vars, lock CORS to ALLOWED_ORIGIN, sslmode=require.
                P1 security items if time. If short on time, demo locally."
      gate: "No secret in client bundle; CORS rejects foreign origin; injected 'ignore instructions'
             line in upload does not change behavior."

  notes:
    - "Frontend phases live in frontend_specs/ (Next.js 4-state UI on Vercel AI SDK), derived from CONTRACT.md."
    - "Before each integration: Context7 MCP resolve-library-id -> get-library-docs."
@end
```
