"""Async SQLAlchemy engine/session + create_all on startup.

Single code path for both targets:
  * DATABASE_URL set  -> Neon Postgres via asyncpg (sslmode honored as ssl=True)
  * DATABASE_URL unset -> local SQLite file (aiosqlite) so the flow runs with no Neon

No migrations (PoC) — tables are created with create_all (spec: requirements.md §13).
"""
from __future__ import annotations

import logging
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.config import get_settings
from backend.models_db import Base

log = logging.getLogger("db")


def _build_url_and_args(raw: str | None) -> tuple[str, dict]:
    """Normalize a connection string and return (sqlalchemy_url, connect_args)."""
    if not raw:
        db_path = (Path(__file__).resolve().parent / "backend_dev.db").as_posix()
        return f"sqlite+aiosqlite:///{db_path}", {}

    url = raw
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        url = "postgresql+asyncpg://" + url[len("postgresql://"):]

    # asyncpg does not understand libpq query params like sslmode/channel_binding.
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query))
    sslmode = query.pop("sslmode", None)
    query.pop("channel_binding", None)
    url = urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment)
    )

    connect_args: dict = {}
    if sslmode and sslmode != "disable":
        connect_args["ssl"] = True  # Neon requires TLS
    return url, connect_args


_settings = get_settings()
_DATABASE_URL, _CONNECT_ARGS = _build_url_and_args(_settings.database_url)

engine = create_async_engine(_DATABASE_URL, connect_args=_CONNECT_ARGS, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def _sync_init(sync_conn) -> None:
    """Create tables; if an existing table is missing expected columns (schema drift
    from a model change), drop the app's tables and recreate them. Prototype data is
    disposable, so this lets a redeploy self-heal without manual migrations."""
    inspector = inspect(sync_conn)
    drift = False
    for table in Base.metadata.sorted_tables:
        if inspector.has_table(table.name):
            existing = {c["name"] for c in inspector.get_columns(table.name)}
            expected = {c.name for c in table.columns}
            if not expected.issubset(existing):
                log.warning("schema drift in '%s' (missing %s) — recreating tables",
                            table.name, expected - existing)
                drift = True
                break
    if drift:
        # Drop any orphaned tables not in models (e.g., old suggestions) with CASCADE
        for table_name in inspector.get_table_names():
            if not any(t.name == table_name for t in Base.metadata.sorted_tables):
                try:
                    log.info("dropping orphaned table '%s'", table_name)
                    sync_conn.execute(text(f"DROP TABLE IF EXISTS \"{table_name}\" CASCADE"))
                except Exception as e:
                    log.warning("failed to drop orphaned table '%s': %s", table_name, e)
        # Drop all model tables with CASCADE
        Base.metadata.drop_all(sync_conn)
    Base.metadata.create_all(sync_conn)


async def init_db() -> None:
    """Create (and, on schema drift, recreate) all tables. Called once on app startup."""
    async with engine.begin() as conn:
        await conn.run_sync(_sync_init)


async def get_session() -> AsyncSession:
    """FastAPI dependency yielding an async session."""
    async with SessionLocal() as session:
        yield session
