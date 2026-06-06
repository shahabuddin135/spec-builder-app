"""P0 security controls: upload validation, safe naming, rate limiter.

These controls are what make an unauthenticated public endpoint acceptable
(this PoC has no auth — see SECURITY.md).
"""
from __future__ import annotations

import re
import uuid
from pathlib import Path

from fastapi import HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.config import (
    ALLOWED_CONTENT_TYPES,
    ALLOWED_EXTENSIONS,
    MAX_UPLOAD_BYTES,
)

# C0/C1 control chars except tab/newline/carriage-return, plus DEL.
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]")

# Per-IP rate limiter. Per-route limits are applied in Phase 2 routes.
limiter = Limiter(key_func=get_remote_address)


def check_extension_and_type(filename: str | None, content_type: str | None) -> None:
    """Allowlist extension AND content-type. Reject everything else with 415."""
    ext = Path(filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Only .txt and .md files are accepted")

    ct = (content_type or "").split(";")[0].strip().lower()
    allowed = ALLOWED_CONTENT_TYPES | {"application/octet-stream"}
    if ct not in allowed:
        raise HTTPException(status_code=415, detail=f"Unsupported content type: {ct}")


def read_validated_text(raw: bytes) -> str:
    """Enforce size, UTF-8, no null bytes; strip control chars. 413/422 on violation."""
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds 256 KB limit")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=422, detail="File is not valid UTF-8 text")
    if "\x00" in text:
        raise HTTPException(status_code=422, detail="File contains null bytes")
    return _CONTROL_RE.sub("", text)


def generate_safe_name(original_name: str | None) -> str:
    """Server-generated UUID filename — user path is never trusted (traversal guard)."""
    ext = Path(original_name or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        ext = ".txt"
    return f"{uuid.uuid4().hex}{ext}"


def sanitize_download_name(name: str) -> str:
    """Whitelist filename chars for Content-Disposition (no separators/traversal)."""
    cleaned = _SAFE_NAME_RE.sub("_", name).lstrip(".")
    return cleaned or "download"
