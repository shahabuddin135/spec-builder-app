"""FastAPI app: CORS, routers, SSE endpoint, exception handlers.

Flow (spec: requirements.md §5, §10): upload -> analyze (Analyst->Strategist, in the
background, streaming events) -> refine (bounded 3) / feedback (self-learning) ->
generate-specs (Spec-Writer) -> download. UI transitions are driven by /events.
No auth (PoC); security rests on the controls in security.py + SECURITY.md.
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import uuid

from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, Request, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy import select

from backend import learning, models_db, security
from backend.agents.analyst import run_analyst
from backend.agents.specwriter import run_specwriter
from backend.agents.strategist import run_strategist
from backend.config import MAX_REFINE_ITERATIONS, get_settings
from backend.db import SessionLocal, init_db
from backend.events import bus, event_stream
from backend.schemas import (
    AnalyzeReq,
    AnalyzeResp,
    BrandCard,
    FeatureCard,
    FeedbackReq,
    GenerateSpecsReq,
    RefineReq,
    RefineResp,
    SpecFile,
    SpecResp,
    Suggestion,
    UploadResp,
)

log = logging.getLogger("main")
settings = get_settings()
limiter = security.limiter

# Strong refs to background tasks so they aren't garbage-collected mid-run.
_bg_tasks: set[asyncio.Task] = set()


def _spawn(coro) -> None:
    task = asyncio.create_task(coro)
    _bg_tasks.add(task)
    task.add_done_callback(_bg_tasks.discard)


def _dump_items(items: list[Suggestion]) -> list[dict]:
    return [s.model_dump(mode="json") for s in items]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Marketing Strategy Spec Generator", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origin],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(Exception)
async def _unhandled(request: Request, exc: Exception):
    log.exception("unhandled error")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


# ---- helpers ----------------------------------------------------------------


async def _latest_suggestion(session, analysis_id: str):
    result = await session.execute(
        select(models_db.Suggestion)
        .where(models_db.Suggestion.analysis_id == analysis_id)
        .order_by(models_db.Suggestion.iteration.desc())
    )
    return result.scalars().first()


async def _run_analysis_pipeline(analysis_id: str, document_id: str) -> None:
    """Analyst -> Strategist, emitting events. Never raises to the loop."""
    try:
        await bus.publish("analysis.started", "Analyzing upload", {"analysis_id": analysis_id})
        async with SessionLocal() as session:
            doc = await session.get(models_db.Document, document_id)
            if doc is None:
                await bus.publish("error", "Document missing", {"analysis_id": analysis_id})
                return
            analyst_out = await run_analyst(doc.content)
            session.add(
                models_db.Analysis(
                    id=analysis_id,
                    document_id=document_id,
                    feature_card=analyst_out.feature_card.model_dump(),
                    brand_card=analyst_out.brand_card.model_dump(),
                )
            )
            await session.commit()
            await bus.publish(
                "analysis.done",
                "Analysis complete",
                {"analysis_id": analysis_id, "persona": analyst_out.feature_card.persona},
            )

            smap = await learning.stats_map(session)
            items = await run_strategist(
                analyst_out.feature_card,
                analyst_out.brand_card,
                smap,
                learning.top3_lines(smap),
            )
            session.add(
                models_db.Suggestion(
                    analysis_id=analysis_id, items=_dump_items(items), iteration=0, status="proposed"
                )
            )
            await session.commit()
        await bus.publish(
            "suggestions.ready",
            "Suggestions ready",
            {"analysis_id": analysis_id, "iteration": 0, "items": _dump_items(items)},
        )
    except Exception:
        log.exception("analysis pipeline failed")
        await bus.publish("error", "Analysis failed", {"analysis_id": analysis_id})


async def _replay_cached(analysis_id: str) -> None:
    async with SessionLocal() as session:
        analysis = await session.get(models_db.Analysis, analysis_id)
        latest = await _latest_suggestion(session, analysis_id)
    persona = (analysis.feature_card or {}).get("persona") if analysis else None
    await bus.publish("analysis.done", "Cached analysis", {"analysis_id": analysis_id, "persona": persona})
    if latest:
        await bus.publish(
            "suggestions.ready",
            "Cached suggestions",
            {"analysis_id": analysis_id, "iteration": latest.iteration, "items": latest.items},
        )


# ---- routes -----------------------------------------------------------------


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "llm_enabled": settings.has_llm}


@app.get("/events")
async def events(request: Request):
    return StreamingResponse(
        event_stream(request),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/upload", response_model=UploadResp)
async def upload(file: UploadFile = File(...)) -> UploadResp:
    security.check_extension_and_type(file.filename, file.content_type)
    raw = await file.read()
    text = security.read_validated_text(raw)  # 413 / 422
    sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()

    async with SessionLocal() as session:
        existing = (
            await session.execute(select(models_db.Document).where(models_db.Document.sha256 == sha256))
        ).scalars().first()
        if existing:  # identical upload -> cache (spec §7.6)
            return UploadResp(document_id=existing.id)
        doc = models_db.Document(
            safe_name=security.generate_safe_name(file.filename), content=text, sha256=sha256
        )
        session.add(doc)
        await session.commit()
        await session.refresh(doc)
        return UploadResp(document_id=doc.id)


@app.post("/analyze", response_model=AnalyzeResp)
@limiter.limit(settings.rate_limit)
async def analyze(request: Request, body: AnalyzeReq) -> AnalyzeResp:
    async with SessionLocal() as session:
        doc = await session.get(models_db.Document, body.document_id)
        if doc is None:
            raise HTTPException(status_code=404, detail="document not found")
        existing = (
            await session.execute(
                select(models_db.Analysis).where(models_db.Analysis.document_id == doc.id)
            )
        ).scalars().first()
        if existing:  # cached analysis -> replay events, no re-run
            _spawn(_replay_cached(existing.id))
            return AnalyzeResp(analysis_id=existing.id)

    analysis_id = str(uuid.uuid4())
    _spawn(_run_analysis_pipeline(analysis_id, body.document_id))
    return AnalyzeResp(analysis_id=analysis_id)


@app.post("/refine", response_model=RefineResp)
@limiter.limit(settings.rate_limit)
async def refine(request: Request, body: RefineReq) -> RefineResp:
    async with SessionLocal() as session:
        analysis = await session.get(models_db.Analysis, body.analysis_id)
        if analysis is None:
            raise HTTPException(status_code=404, detail="analysis not found")
        latest = await _latest_suggestion(session, body.analysis_id)
        current_iter = latest.iteration if latest else 0
        if current_iter >= MAX_REFINE_ITERATIONS:
            raise HTTPException(status_code=409, detail="Refine limit (3) reached")
        new_iter = current_iter + 1

        feature_card = FeatureCard(**analysis.feature_card)
        brand_card = BrandCard(**analysis.brand_card)
        smap = await learning.stats_map(session)
        items = await run_strategist(
            feature_card, brand_card, smap, learning.top3_lines(smap), feedback=body.feedback
        )
        session.add(
            models_db.Suggestion(
                analysis_id=body.analysis_id, items=_dump_items(items), iteration=new_iter, status="refined"
            )
        )
        await session.commit()

    await bus.publish(
        "suggestions.ready",
        "Refined suggestions",
        {"analysis_id": body.analysis_id, "iteration": new_iter, "items": _dump_items(items)},
    )
    return RefineResp(analysis_id=body.analysis_id, iteration=new_iter)


@app.post("/feedback", status_code=204)
async def feedback(body: FeedbackReq) -> Response:
    async with SessionLocal() as session:
        await learning.record(session, body.strategy_id.value, body.action)
    return Response(status_code=204)


@app.post("/generate-specs", response_model=SpecResp)
@limiter.limit(settings.rate_limit)
async def generate_specs(request: Request, body: GenerateSpecsReq) -> SpecResp:
    async with SessionLocal() as session:
        analysis = await session.get(models_db.Analysis, body.analysis_id)
        if analysis is None:
            raise HTTPException(status_code=404, detail="analysis not found")
        latest = await _latest_suggestion(session, body.analysis_id)
        all_items = [Suggestion(**it) for it in (latest.items if latest else [])]
        approved_set = set(body.approved_ids)
        approved = [s for s in all_items if s.strategy_id.value in approved_set] or all_items

        feature_card = FeatureCard(**analysis.feature_card)
        brand_card = BrandCard(**analysis.brand_card)
        files: list[SpecFile] = await run_specwriter(feature_card, brand_card, approved)

        spec = models_db.Spec(analysis_id=body.analysis_id, files=[f.model_dump() for f in files])
        session.add(spec)
        await session.commit()
        await session.refresh(spec)
        spec_id = spec.id

    await bus.publish(
        "spec.generated",
        "Specs generated",
        {"spec_id": spec_id, "files": [{"name": f.name, "mime": f.mime} for f in files]},
    )
    return SpecResp(spec_id=spec_id, files=files)


@app.get("/specs/{spec_id}/{name}")
async def download_spec(spec_id: str, name: str) -> Response:
    async with SessionLocal() as session:
        spec = await session.get(models_db.Spec, spec_id)
    if spec is None:
        raise HTTPException(status_code=404, detail="spec not found")
    target = next((f for f in spec.files if f["name"] == name), None)
    if target is None:
        raise HTTPException(status_code=404, detail="file not found")
    safe = security.sanitize_download_name(target["name"])
    return Response(
        content=target["content"],
        media_type=target["mime"],
        headers={"Content-Disposition": f'attachment; filename="{safe}"'},
    )
