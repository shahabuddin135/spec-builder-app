"""Deterministic text -> FeatureCard (NO LLM).

This is the fallback that keeps the whole product working with the LLM key
removed. Pure functions: same input always yields the same output.
"""
from __future__ import annotations

import re

from backend.schemas import BrandCard, FeatureCard, Signals

# Occurrences of cue words that push a signal toward ~1.0.
_NORM = 4.0

_SIGNAL_KEYWORDS: dict[str, list[str]] = {
    "price_sens": ["discount", "cheap", "price", "deal", "save", "coupon",
                   "budget", "sale", "%", "affordable"],
    "loyalty": ["loyal", "member", "reward", "points", "vip", "returning",
                "subscriber", "repeat", "retention"],
    "recency": ["today", "this week", "recent", "just", "latest", "now",
                "yesterday"],
    "novelty": ["new", "novel", "innovative", "fresh", "launch", "trend",
                "cutting-edge", "beta"],
    "engage": ["click", "open", "engage", "share", "comment", "like",
               "follow", "active", "visit", "session"],
}

_NEW_KEYWORDS = ["new customer", "first-time", "first time", "sign up", "signup",
                 "welcome", "trial", "just joined", "new user", "prospect"]

_PERSONA = {
    "price_sens": "Deal Seeker",
    "loyalty": "Loyal Advocate",
    "recency": "Recently Active",
    "novelty": "Novelty Chaser",
    "engage": "Highly Engaged",
}

_HEX_RE = re.compile(r"#[0-9a-fA-F]{6}\b")
_TONE_CUES = {
    "luxury": "premium", "premium": "premium", "playful": "playful",
    "fun": "playful", "professional": "professional", "bold": "bold",
    "minimal": "minimal", "friendly": "friendly",
}
_RESTRICT_MARKERS = ["avoid:", "do not use:", "don't use:", "banned:",
                     "restricted:", "never say:", "prohibited:"]


def build_feature_card(text: str) -> FeatureCard:
    low = text.lower()
    scores = {
        sig: round(min(1.0, sum(low.count(k) for k in kws) / _NORM), 2)
        for sig, kws in _SIGNAL_KEYWORDS.items()
    }
    is_new = any(k in low for k in _NEW_KEYWORDS)
    signals = Signals(is_new=is_new, **scores)
    return FeatureCard(
        persona=_persona(scores, is_new),
        f=signals,
        tags=_tags(scores, is_new),
    )


def _persona(scores: dict[str, float], is_new: bool) -> str:
    if is_new and scores["loyalty"] < 0.3:
        return "New Prospect"
    top = max(scores, key=lambda k: scores[k])
    if scores[top] == 0.0:
        return "General Audience"
    return _PERSONA[top]


def _tags(scores: dict[str, float], is_new: bool) -> list[str]:
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    tags = [k for k, v in ranked if v >= 0.5][:4]
    if is_new and len(tags) < 4 and "new" not in tags:
        tags.append("new")
    return tags[:4]


def extract_brand_card_defaults(text: str) -> BrandCard:
    """Deterministic baseline brand card; the LLM Analyst refines it later."""
    low = text.lower()
    palette = list(dict.fromkeys(_HEX_RE.findall(text)))[:5]
    tone = "friendly-professional"
    for cue, mapped in _TONE_CUES.items():
        if cue in low:
            tone = mapped
            break
    return BrandCard(tone=tone, palette=palette, restricted_keywords=_restricted(text))


def _restricted(text: str) -> list[str]:
    out: list[str] = []
    for line in text.splitlines():
        ll = line.lower()
        for marker in _RESTRICT_MARKERS:
            if marker in ll:
                tail = line[ll.index(marker) + len(marker):]
                out += [w.strip().strip(".") for w in re.split(r"[,;]", tail) if w.strip()]
    seen: list[str] = []
    for w in out:
        if w and w.lower() not in {s.lower() for s in seen}:
            seen.append(w)
    return seen[:10]
