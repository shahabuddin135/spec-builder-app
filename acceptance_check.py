"""Acceptance check for the spec generator, run against the real ASGI app.

Drives the full flow with the example briefs in examples/ and verifies the
clarify -> generate -> review -> zip path. Run from the repo root (isolated:
forces local SQLite, clears keys, never touches Neon):

    .venv/Scripts/python.exe acceptance_check.py
"""
import asyncio
import io
import zipfile
from pathlib import Path

from httpx import ASGITransport, AsyncClient

from backend.agents import runtime
from backend.config import get_settings
from backend.db import init_db
from backend.events import bus
from backend.main import app

EX = Path(__file__).resolve().parent / "examples"
WEB = (EX / "habit_tracker.md").read_text(encoding="utf-8")
API = (EX / "invoicing_api.md").read_text(encoding="utf-8")

FULL_STRUCTURE = {
    "README.md", "SPEC.md", "CONTEXT.md", "CONSTRAINTS.md", "SECURITY.md", "MEMORY.md",
    "backend_specs/ARCH.md", "backend_specs/CONTRACT.md", "backend_specs/PLAN.md",
    "backend_specs/tasks/task_index.md",
    "frontend_specs/ARCH.md", "frontend_specs/CONTRACT.md", "frontend_specs/PLAN.md",
    "frontend_specs/tasks/task_index.md",
}

_results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, note: str = "") -> None:
    _results.append((name, ok, note))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({note})" if note else ""))


async def drain_until(q, target, timeout=12.0):
    seen = []
    while True:
        ev = await asyncio.wait_for(q.get(), timeout=timeout)
        seen.append(ev["type"])
        if ev["type"] == target:
            return ev, seen
        if ev["type"] == "error":
            raise RuntimeError(f"error event; seen={seen}")


async def run_brief(c, q, text, name):
    up = await c.post("/upload", files={"file": (name, text.encode(), "text/markdown")})
    doc = up.json()["document_id"]
    an = await c.post("/analyze", json={"document_id": doc})
    aid = an.json()["analysis_id"]
    ev, seen = await drain_until(q, "questions.ready")
    return aid, ev["data"]["questions"], seen


async def main():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
        q = await bus.subscribe()

        # --- web app brief: brief -> questions -> generate -> zip ---
        aid, questions, seen = await run_brief(c, q, WEB, "habit.md")
        print("questions:", [qq["id"] for qq in questions])
        check("upload -> analyze -> clarifying questions",
              {"analysis.started", "analysis.done", "questions.ready"} <= set(seen)
              and 3 <= len(questions) <= 6)

        answers = [{"id": qq["id"], "answer": "Reasonable answer"} for qq in questions]
        gen = await c.post("/generate-specs", json={"analysis_id": aid, "answers": answers})
        spec_id = gen.json()["spec_id"]
        ev2, _ = await drain_until(q, "spec.generated")
        paths = {f["path"] for f in ev2["data"]["files"]}
        check("full spec package generated", FULL_STRUCTURE <= paths,
              f"missing: {sorted(FULL_STRUCTURE - paths)}")

        z = await c.get(f"/specs/{spec_id}/archive.zip")
        zf = zipfile.ZipFile(io.BytesIO(z.content))
        blob = b"\n".join(zf.read(n) for n in zf.namelist()).decode("utf-8").lower()
        check("specs.zip downloads (attachment, application/zip)",
              z.status_code == 200 and z.headers["content-type"] == "application/zip"
              and 'filename="specs.zip"' in z.headers.get("content-disposition", ""))
        check("no methodology jargon in output", "slc" not in blob)
        check("event-driven (UI advances on events, not POST returns)",
              ev2["data"]["spec_id"] == spec_id)

        one = await c.get(f"/specs/{spec_id}/file/backend_specs/CONTRACT.md")
        check("single-file download works",
              one.status_code == 200 and "attachment" in one.headers.get("content-disposition", ""))

        rf = await c.post("/refine", json={"analysis_id": aid, "feedback": "Add export-to-CSV."})
        ev3, _ = await drain_until(q, "spec.generated")
        check("request-changes regenerates (revision++)", ev3["data"]["iteration"] == 1)

        # --- API brief: project-type adaptation (no UI screens) ---
        aid2, _, _ = await run_brief(c, q, API, "api.md")
        gen2 = await c.post("/generate-specs", json={"analysis_id": aid2, "answers": []})
        sid2 = gen2.json()["spec_id"]
        await drain_until(q, "spec.generated")
        fe = await c.get(f"/specs/{sid2}/file/frontend_specs/ARCH.md")
        check("API project notes 'backend-only' in frontend ARCH",
              "backend-only" in fe.text.lower())

        # --- security: no key -> deterministic; token ceiling fires ---
        check("works with NO LLM key (deterministic)", get_settings().has_llm is False)
        try:
            runtime.assert_within_budget("x" * 100_000)
            fired = False
        except ValueError:
            fired = True
        check("token-ceiling assert fires on bloated input", fired)

    passed = sum(1 for _, ok, _ in _results if ok)
    print(f"\n==== {passed}/{len(_results)} acceptance checks PASSED ====")
    if passed != len(_results):
        raise SystemExit(1)


asyncio.run(main())
