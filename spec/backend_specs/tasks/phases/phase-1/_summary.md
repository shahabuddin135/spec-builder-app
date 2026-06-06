```slc
@block PHASE phase_1_summary
priority: high
intent: "Phase 1 overview and progress — Foundation (NO LLM)"
scope: phase-1

content:
  name: "Foundation (NO LLM)"
  description: "Deterministic core: scaffold, settings, async DB, models, schemas, upload
                security, deterministic FeatureCard ingest, fixed strategy seed."
  total_tasks: 9
  completed: 9

  task_order:
    - 1.1_init_project
    - 1.2_config
    - 1.3_db
    - 1.4_models_db
    - 1.5_schemas
    - 1.6_security
    - 1.7_ingest
    - 1.8_strategies_seed
    - 1.9_verify_foundation

  exit_gate: "curl uploads a .txt -> FeatureCard produced; a .pdf or >256KB file rejected (415/413).
              No LLM involved anywhere in this phase."
@end
```
