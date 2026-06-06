# SPEC — SpecForge

Internal specification for the SpecForge app (the spec generator itself). Read order:

1. `CONTEXT.md` — goal and scope.
2. `CONSTRAINTS.md` — tech, scale, hard rules.
3. `SECURITY.md` — security rules.
4. `MEMORY.md` — frozen decisions and assumptions.
5. `backend_specs/ARCH.md` → `backend_specs/CONTRACT.md` → `backend_specs/PLAN.md`.
6. `backend_specs/tasks/task_index.md` — task status.

The product, the UI, and the spec packages it generates contain no methodology jargon.
The frontend derives from `backend_specs/CONTRACT.md`.
