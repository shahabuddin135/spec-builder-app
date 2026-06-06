"""SQLAlchemy 2.0 models for the spec generator.

documents -> analyses (parsed brief + clarifying questions + answers) -> specs
(the rendered file package). JSON columns use JSONB on Postgres, JSON on SQLite.
UUID primary keys are stored as 36-char strings for portability.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# JSONB where supported, JSON elsewhere.
JSONVariant = JSON().with_variant(JSONB(), "postgresql")


def _uuid() -> str:
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    safe_name: Mapped[str] = mapped_column(Text)          # server-generated UUID name
    content: Mapped[str] = mapped_column(Text)            # raw brief — never sent verbatim to an LLM
    sha256: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.id"))
    brief: Mapped[dict] = mapped_column(JSONVariant)              # parsed ProjectBrief
    questions: Mapped[list] = mapped_column(JSONVariant, default=list)  # clarifying questions
    answers: Mapped[list] = mapped_column(JSONVariant, default=list)    # [{id, answer}]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Spec(Base):
    __tablename__ = "specs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    analysis_id: Mapped[str] = mapped_column(ForeignKey("analyses.id"))
    files: Mapped[list] = mapped_column(JSONVariant)     # [{path, mime, content}]
    iteration: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
