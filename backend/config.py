"""Env-loaded settings, token budgets, and constants.

Canonical env vars ONLY (never invent names): DATABASE_URL, LLM_API_KEY,
GROQ_API_KEY, OPENAI_API_KEY, ALLOWED_ORIGIN, RATE_LIMIT.  (spec: CONSTRAINTS.md)
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# ---- Constants (DO NOT CHANGE without a MEMORY.md entry) --------------------
MAX_AGENT_INPUT_TOKENS = 800          # runtime.py estimates len//4 and RAISES if exceeded
MAX_OUTPUT_TOKENS = 256               # agent outputs are small JSON
MAX_UPLOAD_BYTES = 256 * 1024         # 256 KB upload ceiling
MAX_REFINE_ITERATIONS = 3             # /refine is bounded
LLM_TIMEOUT_SECONDS = 30              # hard ceiling on a single model call (anti-hang)
ANALYST_INPUT_CHARS = 1800            # bounded upload excerpt sent to the Analyst (<=800 tokens)
ALLOWED_EXTENSIONS = {".txt", ".md"}
# Browsers/curl are inconsistent for .md; octet-stream/empty are tolerated only
# when the extension already passed. application/pdf and friends are rejected.
ALLOWED_CONTENT_TYPES = {"text/plain", "text/markdown", "text/x-markdown", ""}

_ENV_FILE = Path(__file__).resolve().parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Persistence (unset -> local SQLite fallback, see db.py)
    database_url: str | None = None

    # LLM gateway keys (all unset -> deterministic fallback path)
    llm_api_key: str | None = None
    groq_api_key: str | None = None
    openai_api_key: str | None = None

    # Web
    allowed_origin: str = "http://localhost:3000"
    rate_limit: str = "20/minute"

    # Model routing (LiteLLM ids; verify against Context7 before trusting)
    groq_model: str = "groq/llama-3.3-70b-versatile"
    openai_model: str = "gpt-4o-mini"

    @property
    def has_llm(self) -> bool:
        """True only when a usable model key is present. Drives the fallback path."""
        return bool(self.groq_api_key or self.openai_api_key or self.llm_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
