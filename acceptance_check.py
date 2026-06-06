"""Acceptance check for requirements.md §12, run against the real ASGI app.

Drives the full flow with the realistic example uploads in examples/ and maps each
result to a §12 criterion. This is the allowed "acceptance check" (requirements.md §13);
it is NOT a unit-test suite. Run from the repo root:

    .venv/Scripts/python.exe acceptance_check.py
"""
import asyncio
import json
from pathlib import Path

from httpx import ASGITransport, AsyncClient

from backend.agents import runtime
from backend.config import get_settings
from backend.db import init_db
from backend.events import bus
from backend.ingest import build_feature_card, extract_brand_card_defaults
from backend.main import app

EX = Path(__file__).resolve().parent / "examples"
ACME = (EX / "acme_coffee_club.md").read_text(encoding="utf-8")
AURORA = (EX / "aurora_skincare.md").read_text(encoding="utf-8")

_results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, note: str = "") -> None:
    _results.append((name, ok, note))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({note})" if note else ""))


async def drain_until(q, target, timeout=10.0):
    seen = []
    while True:
        ev = await asyncio.wait_for(q.get(), timeout=timeout)
        seen.append(ev["type"])
        if ev["type"] == target:
            return ev, seen
        if ev["type"] == "error":
            raise RuntimeError(f"pipeline error; seen={seen}")


async def upload_analyze(c, q, text, name):
    up = await c.post("/upload", files={"file": (name, text.encode(), "text/plain")})
    doc = up.json()["document_id"]
    an = await c.post("/analyze", json={"document_id": doc})
    aid = an.json()["analysis_id"]
    ev, seen = await drain_until(q, "suggestions.ready")
    return doc, aid, ev["data"]["items"], seen


async def main():
    await init_db()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as c:
        q = await bus.subscribe()

        # ---- §12.1 upload -> FeatureCard; raw text never sent to an LLM ----
        doc_a, aid_a, items_a, seen_a = await upload_analyze(c, q, ACME, "acme.md")
        fc_a = build_feature_card(ACME)
        print("\nACME FeatureCard:\n" + json.dumps(fc_a.model_dump(), indent=2))
        print("ACME ranked:", [i["strategy_id"] for i in items_a])
        check("§12.1 upload -> FeatureCard", bool(doc_a) and "persona" in fc_a.model_dump())

        r415 = await c.post("/upload", files={"file": ("x.pdf", b"%PDF-1.4", "application/pdf")})
        r413 = await c.post("/upload", files={"file": ("big.txt", b"a" * (256 * 1024 + 1), "text/plain")})
        r422 = await c.post("/upload", files={"file": ("n.txt", b"hi\x00there", "text/plain")})
        check("§12.1 reject .pdf/oversize/binary",
              r415.status_code == 415 and r413.status_code == 413 and r422.status_code == 422,
              f"{r415.status_code}/{r413.status_code}/{r422.status_code}")

        # ---- §12.3 UI advances on events ----
        check("§12.3 flow advances on events",
              {"analysis.started", "analysis.done", "suggestions.ready"} <= set(seen_a), str(seen_a))

        # ---- §12.2 second upload differs; restricted keyword never appears ----
        doc_b, aid_b, items_b, seen_b = await upload_analyze(c, q, AURORA, "aurora.md")
        fc_b = build_feature_card(AURORA)
        bc_b = extract_brand_card_defaults(AURORA)
        print("\nAURORA FeatureCard:\n" + json.dumps(fc_b.model_dump(), indent=2))
        print("AURORA brand restricted_keywords:", bc_b.restricted_keywords)
        print("AURORA ranked:", [i["strategy_id"] for i in items_b])
        check("§12.2 different uploads -> different suggestions",
              [i["strategy_id"] for i in items_a] != [i["strategy_id"] for i in items_b])

        restricted = {w.lower() for w in
                      extract_brand_card_defaults(ACME).restricted_keywords + bc_b.restricted_keywords}
        copy_blob = " ".join(i["title"] + " " + i["rationale"] for i in items_a + items_b).lower()
        check("§12.2 restricted keyword absent from suggestions",
              all(w not in copy_blob for w in restricted), f"restricted={sorted(restricted)}")

        # ---- §12.7 prompt-injection ignored ----
        check("§12.7 injected 'ignore instructions' had no effect (no PWNED)", "pwned" not in copy_blob)

        # ---- §7.6 identical upload is cached ----
        dup = await c.post("/upload", files={"file": ("acme2.md", ACME.encode(), "text/plain")})
        check("§7.6 identical upload cached (same document_id)", dup.json()["document_id"] == doc_a)

        # ---- §12.4 approve + refine + generate + download ----
        await c.post("/feedback", json={"strategy_id": items_b[0]["strategy_id"], "action": "approve"})
        rf = await c.post("/refine", json={"analysis_id": aid_b, "feedback": "lean into welcome and novelty"})
        await drain_until(q, "suggestions.ready")
        gs = await c.post("/generate-specs", json={
            "analysis_id": aid_b,
            "approved_ids": [items_b[0]["strategy_id"], items_b[1]["strategy_id"]],
        })
        spec = gs.json()
        await drain_until(q, "spec.generated")
        names = {f["name"] for f in spec["files"]}
        md = next(f["content"] for f in spec["files"] if f["name"].endswith(".md"))
        dl = await c.get(f"/specs/{spec['spec_id']}/marketing-strategy-spec.md")
        check("§12.4 specs generated + downloadable",
              names == {"marketing-strategy-spec.md", "personalization-rules.json", "brand-card.json"}
              and rf.json()["iteration"] == 1 and dl.status_code == 200
              and "attachment" in dl.headers.get("content-disposition", "")
              and dl.headers["content-type"].startswith("text/markdown"))
        check("§12.2 restricted keyword absent from generated spec",
              all(w not in md.lower() for w in restricted))
        print("\n----- generated marketing-strategy-spec.md (Aurora) -----\n" + md
              + "\n---------------------------------------------------------")

        # ---- §12.5 approve/reject re-ranks on re-run (self-learning) ----
        base_rank = [i["strategy_id"] for i in items_b]
        target, above = base_rank[-1], base_rank[-2]
        for _ in range(8):
            await c.post("/feedback", json={"strategy_id": target, "action": "approve"})
        for _ in range(6):
            await c.post("/feedback", json={"strategy_id": above, "action": "reject"})
        _, _, items_b2, _ = await upload_analyze(c, q, AURORA + "\n<!-- variant -->", "aurora_v2.md")
        new_rank = [i["strategy_id"] for i in items_b2]
        print(f"self-learning: '{target}' rank {base_rank.index(target)} -> {new_rank.index(target)}")
        check("§12.5 approve/reject re-ranks (self-learning)",
              new_rank.index(target) < base_rank.index(target) and new_rank != base_rank,
              f"{target}: {base_rank.index(target)} -> {new_rank.index(target)}")

        # ---- §12.6 deterministic flow w/o key + token ceiling ----
        check("§12.6 full flow works with NO LLM key (deterministic)",
              get_settings().has_llm is False and bool(items_a))
        try:
            runtime.assert_within_budget("x" * 100_000)
            fired = False
        except ValueError:
            fired = True
        check("§12.6 token-ceiling assert fires on bloated input", fired)

        # ---- §12.7 CORS rejects a foreign origin ----
        pre = await c.options("/analyze", headers={
            "Origin": "http://evil.example", "Access-Control-Request-Method": "POST"})
        aco = pre.headers.get("access-control-allow-origin")
        check("§12.7 CORS rejects foreign origin", aco != "http://evil.example", f"allow-origin={aco}")

    passed = sum(1 for _, ok, _ in _results if ok)
    print(f"\n==== {passed}/{len(_results)} acceptance checks PASSED ====")
    if passed != len(_results):
        raise SystemExit(1)


asyncio.run(main())
