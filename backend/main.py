"""FastAPI app: spec generator + reviewer.

Flow: upload brief -> analyze (parse + clarifying questions) -> generate-specs
(answers -> full package) -> refine (request changes -> regenerate) -> download
specs.zip. UI transitions are driven by SSE events, not POST returns. No auth (PoC).
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

from backend import models_db, security, specgen
from backend.agents.analyst import run_analyst
from backend.agents.clarifier import run_clarifier
from backend.agents.planner import run_planner
from backend.config import MAX_SPEC_REVISIONS, get_settings
from backend.db import SessionLocal, init_db
from backend.events import bus, event_stream
from backend.schemas import (
    AnalyzeReq,
    AnalyzeResp,
    GenerateReq,
    GenerateResp,
    ProjectBrief,
    RefineReq,
    UploadResp,
)

log = logging.getLogger("main")
settings = get_settings()
limiter = security.limiter

_bg_tasks: set[asyncio.Task] = set()


def _spawn(coro) -> None:
    task = asyncio.create_task(coro)
    _bg_tasks.add(task)
    task.add_done_callback(_bg_tasks.discard)


def _qa_pairs(analysis: models_db.Analysis) -> list[tuple[str, str]]:
    qmap = {q.get("id", ""): q.get("question", "") for q in (analysis.questions or [])}
    pairs: list[tuple[str, str]] = []
    for a in analysis.answers or []:
        qid = a.get("id", "")
        pairs.append((qmap.get(qid, qid), a.get("answer", "")))
    return pairs


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="SpecForge — Spec Generator", version="0.2.0", lifespan=lifespan)

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


# ---- background pipelines ---------------------------------------------------


async def _run_analysis(analysis_id: str, document_id: str) -> None:
    try:
        await bus.publish("analysis.started", "Reading your brief", {"analysis_id": analysis_id})
        async with SessionLocal() as session:
            doc = await session.get(models_db.Document, document_id)
            if doc is None:
                await bus.publish("error", "Document missing", {"analysis_id": analysis_id})
                return
            brief = await run_analyst(doc.content)
            await bus.publish(
                "analysis.done",
                "Brief parsed",
                {"analysis_id": analysis_id, "title": brief.title, "project_type": brief.project_type},
            )
            questions = await run_clarifier(brief)
            session.add(
                models_db.Analysis(
                    id=analysis_id,
                    document_id=document_id,
                    brief=brief.model_dump(),
                    questions=[q.model_dump() for q in questions],
                    answers=[],
                )
            )
            await session.commit()
        await bus.publish(
            "questions.ready",
            "A few quick questions",
            {"analysis_id": analysis_id, "questions": [q.model_dump() for q in questions]},
        )
    except Exception:
        log.exception("analysis pipeline failed")
        await bus.publish("error", "Analysis failed", {"analysis_id": analysis_id})


async def _run_generate(
    spec_id: str,
    analysis_id: str,
    answers: list | None,
    feedback: str,
    iteration: int,
) -> None:
    try:
        await bus.publish("spec.generating", "Writing your specs", {"analysis_id": analysis_id})
        async with SessionLocal() as session:
            analysis = await session.get(models_db.Analysis, analysis_id)
            if analysis is None:
                await bus.publish("error", "Analysis missing", {"analysis_id": analysis_id})
                return
            if answers is not None:
                analysis.answers = [a.model_dump() for a in answers]
                await session.commit()
            brief = ProjectBrief(**analysis.brief)
            qa = _qa_pairs(analysis)
            spec = await run_planner(brief, qa, feedback or "")
            files = [f.model_dump() for f in specgen.render_files(spec)]
            session.add(
                models_db.Spec(id=spec_id, analysis_id=analysis_id, files=files, iteration=iteration)
            )
            await session.commit()
        await bus.publish(
            "spec.generated",
            "Specs ready",
            {
                "spec_id": spec_id,
                "iteration": iteration,
                "title": spec.title,
                "files": [{"path": f["path"], "mime": f["mime"]} for f in files],
            },
        )
    except Exception:
        log.exception("generate pipeline failed")
        await bus.publish("error", "Spec generation failed", {"analysis_id": analysis_id})


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
        if existing:
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
    analysis_id = str(uuid.uuid4())
    _spawn(_run_analysis(analysis_id, body.document_id))
    return AnalyzeResp(analysis_id=analysis_id)


@app.post("/generate-specs", response_model=GenerateResp)
@limiter.limit(settings.rate_limit)
async def generate_specs(request: Request, body: GenerateReq) -> GenerateResp:
    async with SessionLocal() as session:
        analysis = await session.get(models_db.Analysis, body.analysis_id)
        if analysis is None:
            raise HTTPException(status_code=404, detail="analysis not found")
    spec_id = str(uuid.uuid4())
    _spawn(_run_generate(spec_id, body.analysis_id, body.answers, "", 0))
    return GenerateResp(spec_id=spec_id)


@app.post("/refine", response_model=GenerateResp)
@limiter.limit(settings.rate_limit)
async def refine(request: Request, body: RefineReq) -> GenerateResp:
    async with SessionLocal() as session:
        analysis = await session.get(models_db.Analysis, body.analysis_id)
        if analysis is None:
            raise HTTPException(status_code=404, detail="analysis not found")
        latest = (
            await session.execute(
                select(models_db.Spec)
                .where(models_db.Spec.analysis_id == body.analysis_id)
                .order_by(models_db.Spec.iteration.desc())
            )
        ).scalars().first()
        iteration = (latest.iteration if latest else 0) + 1
        if iteration > MAX_SPEC_REVISIONS:
            raise HTTPException(status_code=409, detail="Revision limit reached")
    spec_id = str(uuid.uuid4())
    _spawn(_run_generate(spec_id, body.analysis_id, None, body.feedback, iteration))
    return GenerateResp(spec_id=spec_id)


@app.get("/specs/{spec_id}/archive.zip")
async def download_zip(spec_id: str) -> Response:
    async with SessionLocal() as session:
        spec = await session.get(models_db.Spec, spec_id)
    if spec is None:
        raise HTTPException(status_code=404, detail="spec not found")
    data = specgen.build_zip(spec.files)
    return Response(
        content=data,
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="specs.zip"'},
    )


@app.get("/specs/{spec_id}/file/{file_path:path}")
async def download_file(spec_id: str, file_path: str) -> Response:
    async with SessionLocal() as session:
        spec = await session.get(models_db.Spec, spec_id)
    if spec is None:
        raise HTTPException(status_code=404, detail="spec not found")
    target = next((f for f in spec.files if f["path"] == file_path), None)
    if target is None:
        raise HTTPException(status_code=404, detail="file not found")
    name = security.sanitize_download_name(file_path.split("/")[-1])
    return Response(
        content=target["content"],
        media_type=target["mime"],
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )
