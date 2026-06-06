"""Turn a ProjectSpec into a full markdown spec package and a downloadable zip.

`deterministic_spec` builds a complete spec from the brief + answers with no LLM
(the planner's fallback). `normalize_spec` merges LLM output over that fallback.
`render_files` writes the file tree (clean markdown — no methodology jargon).
"""
from __future__ import annotations

import datetime
import io
import re
import zipfile

from backend.schemas import Endpoint, Entity, Phase, ProjectBrief, ProjectSpec, SpecFile

_ENTITY_NOUNS = [
    "task", "note", "habit", "recipe", "event", "order", "product", "message",
    "project", "post", "comment", "invoice", "ticket", "booking", "appointment",
    "expense", "workout", "contact", "document", "article", "review", "payment",
    "customer", "lesson", "course", "poll", "photo", "album", "playlist", "song",
]


# ---- helpers ----------------------------------------------------------------


def _bullets(items: list, empty: str = "_None specified._") -> str:
    rows = [f"- {str(i).strip()}" for i in items if str(i).strip()]
    return "\n".join(rows) if rows else empty


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "item"


def _plural(name: str) -> str:
    s = _slug(name)
    return s + "es" if s.endswith(("s", "x", "ch", "sh")) else s + "s"


def _split_items(text: str) -> list[str]:
    parts = re.split(r"[\n;,]| and ", text)
    return [p.strip(" .-\t") for p in parts if p.strip(" .-\t")]


def _find_answer(qa: list[tuple[str, str]], *keys: str) -> str:
    for q, a in qa:
        if a.strip() and any(k in q.lower() for k in keys):
            return a.strip()
    return ""


# ---- deterministic enrichment (planner fallback) ----------------------------


def _default_tech(project_type: str) -> list[str]:
    return {
        "web app": ["Next.js (frontend)", "FastAPI (backend)", "PostgreSQL"],
        "api": ["FastAPI", "PostgreSQL"],
        "cli": ["Python", "Typer"],
        "mobile": ["React Native", "FastAPI", "PostgreSQL"],
    }.get(project_type, ["Next.js (frontend)", "FastAPI (backend)", "PostgreSQL"])


def _derive_entities(brief: ProjectBrief, features: list[str], data_answer: str) -> list[Entity]:
    blob = " ".join(features + [data_answer, brief.summary]).lower()
    found = [n.capitalize() for n in _ENTITY_NOUNS if re.search(rf"\b{n}s?\b", blob)]
    found = list(dict.fromkeys(found))[:5] or ["Item"]

    entities: list[Entity] = []
    if brief.users:
        entities.append(
            Entity(name="User", fields=["id: uuid", "name: string", "email: string", "created_at: timestamp"])
        )
    for n in found:
        if n.lower() == "user":
            continue
        entities.append(
            Entity(name=n, fields=["id: uuid", "title: string", "description: text", "created_at: timestamp"])
        )
    return entities[:6] or [Entity(name="Item", fields=["id: uuid", "title: string", "created_at: timestamp"])]


def _derive_endpoints(entities: list[Entity]) -> list[Endpoint]:
    eps: list[Endpoint] = []
    for e in entities:
        p = _plural(e.name)
        eps += [
            Endpoint(method="GET", path=f"/api/{p}", purpose=f"List {e.name}"),
            Endpoint(method="POST", path=f"/api/{p}", purpose=f"Create {e.name}"),
            Endpoint(method="GET", path=f"/api/{p}/{{id}}", purpose=f"Get one {e.name}"),
            Endpoint(method="PUT", path=f"/api/{p}/{{id}}", purpose=f"Update {e.name}"),
            Endpoint(method="DELETE", path=f"/api/{p}/{{id}}", purpose=f"Delete {e.name}"),
        ]
    return eps[:25]


def _derive_screens(entities: list[Entity]) -> list[str]:
    screens = ["Home / dashboard"]
    for e in entities:
        if e.name == "User":
            continue
        screens += [f"{e.name} list", f"{e.name} detail / edit"]
    return screens[:10]


def _derive_state(entities: list[Entity]) -> list[str]:
    state = ["currentUser", "loading / error flags"]
    for e in entities:
        if e.name == "User":
            continue
        state += [f"{e.name.lower()}List", f"selected{e.name}"]
    return state[:10]


def _default_security(scope_answer: str, project_type: str) -> list[str]:
    sec = [
        "Validate and sanitize all incoming data.",
        "Use parameterized database queries — never build SQL by string concatenation.",
        "Keep secrets in environment variables; never ship them to the client.",
        "Serve over HTTPS only.",
        "Return generic error messages in production; do not leak stack traces.",
    ]
    if "auth" not in scope_answer.lower():
        sec.insert(0, "Authenticate users and enforce per-user authorization on protected routes.")
    return sec


def _derive_phases(features: list[str], entities: list[Entity], has_frontend: bool) -> list[Phase]:
    core_tasks = ["Implement CRUD endpoints for each entity."]
    core_tasks += [f"Build feature: {f}" for f in features[:5]]
    if has_frontend:
        core_tasks.append("Build the core screens and wire them to the API.")
    return [
        Phase(
            name="Phase 1 — Foundation",
            tasks=[
                "Initialize the project and configuration.",
                "Set up the database connection and create tables.",
                "Define data models: " + ", ".join(e.name for e in entities) + ".",
                "Add input validation and error handling.",
            ],
        ),
        Phase(name="Phase 2 — Core features", tasks=core_tasks),
        Phase(
            name="Phase 3 — Polish & ship",
            tasks=[
                "Add acceptance checks for the core flows.",
                "Harden security per SECURITY.md.",
                "Deploy and smoke-test.",
            ],
        ),
    ]


def deterministic_spec(brief: ProjectBrief, qa: list[tuple[str, str]], feedback: str = "") -> ProjectSpec:
    goal = _find_answer(qa, "outcome", "goal", "achieve") or (
        brief.goals[0] if brief.goals else brief.summary
    )
    users = _split_items(_find_answer(qa, "users", "audience")) or brief.users or ["End users"]
    features = _split_items(_find_answer(qa, "feature")) or brief.features or ["Core workflow"]
    non_goals = _split_items(_find_answer(qa, "out of scope", "scope")) or brief.non_goals or [
        "Anything beyond the v1 features listed above"
    ]
    tech = _split_items(_find_answer(qa, "tech", "stack", "hosting")) or brief.tech or _default_tech(
        brief.project_type
    )
    data_answer = _find_answer(qa, "data", "store", "storage")
    scope_answer = _find_answer(qa, "out of scope", "scope")

    entities = _derive_entities(brief, features, data_answer)
    has_frontend = brief.project_type in ("web app", "mobile")
    assumptions = [f"{q.strip().rstrip('?')}: {a.strip()}" for q, a in qa if a.strip()]
    if feedback.strip():
        assumptions.append(f"Requested change applied: {feedback.strip()[:160]}")

    return ProjectSpec(
        title=brief.title,
        summary=brief.summary,
        project_type=brief.project_type,
        goal=goal,
        non_goals=non_goals,
        users=users,
        features=features,
        entities=entities,
        backend_modules=[
            "api (routes + request/response schemas)",
            "models (data layer)",
            "services (business logic)",
            "persistence (database access)",
        ],
        backend_endpoints=_derive_endpoints(entities),
        frontend_screens=_derive_screens(entities) if has_frontend else [],
        frontend_state=_derive_state(entities) if has_frontend else [],
        tech=tech,
        scale=["Single-team / small scale for v1; revisit before heavy load."],
        hard_rules=[
            "No feature outside this spec without updating the spec first.",
            "Keep modules small and single-purpose.",
        ],
        security=_default_security(scope_answer, brief.project_type),
        phases=_derive_phases(features, entities, has_frontend),
        assumptions=assumptions,
    )


def normalize_spec(s: ProjectSpec | None, fb: ProjectSpec) -> ProjectSpec:
    if s is None:
        return fb

    def pick(a, b):
        return a if a else b

    return ProjectSpec(
        title=pick(s.title.strip(), fb.title),
        summary=pick(s.summary.strip(), fb.summary),
        project_type=pick(s.project_type.strip(), fb.project_type),
        goal=pick(s.goal.strip(), fb.goal),
        non_goals=pick(s.non_goals, fb.non_goals)[:10],
        users=pick(s.users, fb.users)[:10],
        features=pick(s.features, fb.features)[:12],
        entities=pick(s.entities, fb.entities)[:8],
        backend_modules=pick(s.backend_modules, fb.backend_modules)[:12],
        backend_endpoints=pick(s.backend_endpoints, fb.backend_endpoints)[:30],
        frontend_screens=pick(s.frontend_screens, fb.frontend_screens)[:14],
        frontend_state=pick(s.frontend_state, fb.frontend_state)[:14],
        tech=pick(s.tech, fb.tech)[:12],
        scale=pick(s.scale, fb.scale)[:6],
        hard_rules=pick(s.hard_rules, fb.hard_rules)[:8],
        security=pick(s.security, fb.security)[:12],
        phases=pick(s.phases, fb.phases)[:6],
        assumptions=pick(s.assumptions, fb.assumptions)[:12],
    )


# ---- markdown rendering -----------------------------------------------------


def _today() -> str:
    return datetime.date.today().isoformat()


def _readme(s: ProjectSpec) -> str:
    return f"""# {s.title} — Specification Package

> {s.summary}

Generated {_today()}. A complete, reviewed specification for **{s.title}** ({s.project_type}).

## How to read this package

1. `SPEC.md` — overview and reading order.
2. `CONTEXT.md` — the goal and what's out of scope.
3. `CONSTRAINTS.md` — tech, scale, and hard rules.
4. `SECURITY.md` — security requirements for all code.
5. `MEMORY.md` — decisions and assumptions to hold steady.
6. `backend_specs/` — architecture, plan, API contract, and tasks.
7. `frontend_specs/` — architecture, plan, contract, and tasks.

Build the backend from its API contract first; the frontend derives from it.
"""


def _spec_md(s: ProjectSpec) -> str:
    return f"""# SPEC.md — {s.title}

Single entry point. Read the files in this order:

1. `CONTEXT.md` — why this exists, the goal, and non-goals.
2. `CONSTRAINTS.md` — hard limits (tech, scale, rules).
3. `SECURITY.md` — security requirements.
4. `MEMORY.md` — frozen decisions and assumptions.
5. `backend_specs/ARCH.md` -> `backend_specs/CONTRACT.md` -> `backend_specs/PLAN.md`.
6. `frontend_specs/ARCH.md` -> `frontend_specs/CONTRACT.md` -> `frontend_specs/PLAN.md`.

## Project at a glance

- **Type:** {s.project_type}
- **Goal:** {s.goal}
- **Primary users:** {", ".join(s.users) or "—"}
- **Core features:**
{_bullets(s.features)}
"""


def _context_md(s: ProjectSpec) -> str:
    return f"""# CONTEXT.md — Goal & Scope

## Goal

{s.goal or s.summary}

## Primary users

{_bullets(s.users)}

## In scope (v1 features)

{_bullets(s.features)}

## Non-goals (explicitly out of scope)

{_bullets(s.non_goals)}
"""


def _constraints_md(s: ProjectSpec) -> str:
    return f"""# CONSTRAINTS.md — Hard Limits

These override plans and tasks.

## Tech

{_bullets(s.tech)}

## Scale

{_bullets(s.scale)}

## Hard rules

{_bullets(s.hard_rules)}
"""


def _security_md(s: ProjectSpec) -> str:
    return f"""# SECURITY.md — Security Requirements

Applies to all code. Refuse to ship anything that violates these.

{_bullets(s.security)}
"""


def _memory_md(s: ProjectSpec) -> str:
    do_not_change = [f"Goal: {s.goal}"] + [f"Non-goal: {n}" for n in s.non_goals[:3]]
    return f"""# MEMORY.md — Decisions & Assumptions

If anything conflicts, this file wins.

## Decisions

- Project type: {s.project_type}
- Tech: {", ".join(s.tech) or "—"}

## Assumptions (from the clarifying answers)

{_bullets(s.assumptions)}

## Do not change

{_bullets(do_not_change)}
"""


def _entity_block(e: Entity) -> str:
    fields = "\n".join(f"  - {f}" for f in e.fields) or "  - id: uuid"
    return f"- **{e.name}**\n{fields}"


def _backend_arch_md(s: ProjectSpec) -> str:
    entities = "\n".join(_entity_block(e) for e in s.entities) or "_No entities defined._"
    return f"""# backend_specs/ARCH.md — Backend Architecture

## Data model

{entities}

## Modules

{_bullets(s.backend_modules)}

## Boundaries

- Routes never contain business logic — they call services.
- Services never build SQL by hand — persistence handles parameterized queries.
- Each entity owns its own model + service.
"""


def _contract_md(s: ProjectSpec) -> str:
    rows = "\n".join(
        f"| {e.method} | `{e.path}` | {e.purpose} |" for e in s.backend_endpoints
    ) or "| — | — | — |"
    return f"""# backend_specs/CONTRACT.md — API Contract

Authoritative for the frontend. JSON request/response; ids are UUIDs.

| Method | Path | Purpose |
|--------|------|---------|
{rows}

All list endpoints support basic pagination; all mutations validate input and return the
affected resource.
"""


def _plan_md(s: ProjectSpec, side: str) -> str:
    blocks = [f"### {p.name}\n\n{_bullets(p.tasks)}" for p in s.phases]
    body = "\n\n".join(blocks) or "_No phases defined._"
    return f"""# {side.lower()}_specs/PLAN.md — {side} Plan

Execution phases for the {side.lower()}. Each phase is shippable before the next.

{body}
"""


def _tasks_md(s: ProjectSpec, side: str) -> str:
    lines = []
    n = 1
    for pi, p in enumerate(s.phases, 1):
        for task in p.tasks:
            lines.append(f"| {pi}.{n} | {task} | todo |")
            n += 1
    table = "\n".join(lines) or "| — | — | — |"
    return f"""# {side.lower()}_specs/tasks/task_index.md — {side} Tasks

| ID | Task | Status |
|----|------|--------|
{table}
"""


def _frontend_arch_md(s: ProjectSpec) -> str:
    if not s.frontend_screens:
        return (
            "# frontend_specs/ARCH.md — Frontend Architecture\n\n"
            f"_No user interface for this {s.project_type}. This project is backend-only; "
            "see `backend_specs/`._\n"
        )
    return f"""# frontend_specs/ARCH.md — Frontend Architecture

Derives from `backend_specs/CONTRACT.md` — no invented endpoints.

## Screens

{_bullets(s.frontend_screens)}

## State

{_bullets(s.frontend_state)}

## Rendering rules

- Render all data as text (escape by default); never inject raw HTML.
- Fetch through a typed API client that mirrors the backend contract.
"""


def _frontend_contract_md(s: ProjectSpec) -> str:
    rows = "\n".join(
        f"| {e.method} | `{e.path}` | {e.purpose} |" for e in s.backend_endpoints
    ) or "| — | — | — |"
    return f"""# frontend_specs/CONTRACT.md — Frontend <-> API

The frontend consumes exactly these backend endpoints. Any mismatch is a bug.

| Method | Path | Purpose |
|--------|------|---------|
{rows}
"""


def render_files(spec: ProjectSpec) -> list[SpecFile]:
    return [
        SpecFile(path="README.md", content=_readme(spec)),
        SpecFile(path="SPEC.md", content=_spec_md(spec)),
        SpecFile(path="CONTEXT.md", content=_context_md(spec)),
        SpecFile(path="CONSTRAINTS.md", content=_constraints_md(spec)),
        SpecFile(path="SECURITY.md", content=_security_md(spec)),
        SpecFile(path="MEMORY.md", content=_memory_md(spec)),
        SpecFile(path="backend_specs/ARCH.md", content=_backend_arch_md(spec)),
        SpecFile(path="backend_specs/CONTRACT.md", content=_contract_md(spec)),
        SpecFile(path="backend_specs/PLAN.md", content=_plan_md(spec, "Backend")),
        SpecFile(path="backend_specs/tasks/task_index.md", content=_tasks_md(spec, "Backend")),
        SpecFile(path="frontend_specs/ARCH.md", content=_frontend_arch_md(spec)),
        SpecFile(path="frontend_specs/CONTRACT.md", content=_frontend_contract_md(spec)),
        SpecFile(path="frontend_specs/PLAN.md", content=_plan_md(spec, "Frontend")),
        SpecFile(path="frontend_specs/tasks/task_index.md", content=_tasks_md(spec, "Frontend")),
    ]


def build_zip(files: list[dict]) -> bytes:
    """Bundle [{path, content}] into specs.zip (under a top-level specs/ folder)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f"specs/{f['path']}", f["content"])
    return buf.getvalue()
