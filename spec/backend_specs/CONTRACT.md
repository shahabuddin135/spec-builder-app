# backend/CONTRACT.md — API Definitions (single-file mode)

> ≤10 endpoints → single file. **Authoritative for the frontend** — the Next.js
> `lib/api.ts` and event reducer MUST mirror this exactly. Derived from `requirements.md` §10.
> Mismatch → `CONTRACT_MISMATCH`.

```slc
@block CONTRACT http_api
priority: critical
intent: "HTTP endpoints — methods, payloads, status codes"
scope: module
depends_on: [ARCH.data_model, ARCH.control_flow]

content:
  base: "FastAPI app; CORS allows ALLOWED_ORIGIN only; no auth (PoC)."

  endpoints:
    - POST /upload:
        body: "multipart/form-data, single file .txt|.md, UTF-8, <=256KB"
        response_200: { document_id: uuid }
        errors: [415 (wrong type/content-type), 413 (too large), 422 (decode/null bytes)]

    - POST /analyze:
        rate_limited: true       # per-IP (RATE_LIMIT)
        body: { document_id: uuid }
        response_200: { analysis_id: uuid }
        emits: [analysis.started, analysis.done, suggestions.ready]
        note: "cached by sha256(content) — identical upload returns existing analysis_id"

    - POST /refine:
        body: { analysis_id: uuid, feedback: string }
        response_200: { analysis_id: uuid, iteration: int }
        emits: [suggestions.ready]
        rule: "max 3 iterations; beyond -> 409 or no-op with current suggestions"

    - POST /feedback:
        body: { strategy_id: string, action: "approve|reject" }
        response_204: true
        effect: "learning.record -> strategy_stats approvals/rejections"

    - POST /generate-specs:
        rate_limited: true
        body: { analysis_id: uuid, approved_ids: "string[]" }
        response_200: { spec_id: uuid, files: "[{name, mime, content}]" }
        emits: [spec.generated]

    - GET /specs/{id}/{name}:
        response_200: "file download"
        headers: { Content-Type: "text/markdown|application/json",
                   Content-Disposition: "attachment; filename=<sanitized>" }
        errors: [404]

    - GET /events:
        response: "text/event-stream (SSE), named events"
@end
```

```slc
@block CONTRACT events
priority: critical
intent: "SSE event names and payload shape the UI subscribes to"
scope: module
depends_on: [CONTRACT.http_api]

content:
  envelope: { type: string, ts: timestamp, msg: string, data: "object?" }

  event_types:
    - analysis.started:  "{ analysis_id }"
    - analysis.done:     "{ analysis_id, persona }"
    - suggestions.ready: "{ analysis_id, iteration, items:[{strategy_id,title,rationale,target_signal,on_brand}] }"
    - spec.generated:    "{ spec_id, files:[{name, mime}] }"   # content fetched via GET /specs

  rule: "Frontend state machine (Upload->Reasoning->Suggestions->Specs) transitions ONLY on these events."
@end
```

```slc
@block CONTRACT agent_io
priority: high
intent: "Structured I/O schemas enforced on every agent call (JSON schema via SDK)"
scope: module
depends_on: [ARCH.agent_boundaries]

content:
  analyst_out:
    feature_card: { persona: string,
                    f: {price_sens: float, loyalty: float, recency: float,
                        novelty: float, engage: float, is_new: bool},
                    tags: "string[<=4]" }
    brand_card:   { tone: string, palette: "string[]", restricted_keywords: "string[]" }

  strategist_out:
    suggestions: "[{ strategy_id: enum(library), title: string,
                     rationale: string(<=160), target_signal: string }]"   # ranked

  specwriter_out:
    files:
      - { name: "marketing-strategy-spec.md", mime: "text/markdown" }
      - { name: "personalization-rules.json", mime: "application/json" }
      - { name: "brand-card.json",            mime: "application/json" }

  on_validation_fail: "deterministic fallback (no retry loop); guardrails reject -> safe template"
@end
```
