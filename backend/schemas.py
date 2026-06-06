"""Pydantic request/response + agent I/O schemas (mirror CONTRACT.md exactly)."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from backend.strategies import StrategyId

# ---- Agent I/O (the compact shapes that flow between agents) ----------------


class Signals(BaseModel):
    price_sens: float = Field(ge=0.0, le=1.0)
    loyalty: float = Field(ge=0.0, le=1.0)
    recency: float = Field(ge=0.0, le=1.0)
    novelty: float = Field(ge=0.0, le=1.0)
    engage: float = Field(ge=0.0, le=1.0)
    is_new: bool


class FeatureCard(BaseModel):
    """The ONLY user representation any agent sees (~40 tokens)."""

    persona: str
    f: Signals
    tags: list[str] = Field(default_factory=list, max_length=4)


class BrandCard(BaseModel):
    tone: str
    palette: list[str] = Field(default_factory=list)
    restricted_keywords: list[str] = Field(default_factory=list)


class Suggestion(BaseModel):
    strategy_id: StrategyId               # enum-constrained to the live library
    title: str
    rationale: str = Field(max_length=160)
    target_signal: str
    on_brand: bool = True


class AnalystOut(BaseModel):
    feature_card: FeatureCard
    brand_card: BrandCard


class StrategistOut(BaseModel):
    suggestions: list[Suggestion]         # ranked


# ---- LLM-facing (tolerant) schemas ------------------------------------------
# Models derive their tool/JSON schema from these, so they carry NO constraints
# (no enum, range, or length) — that way the provider never rejects the model's
# own output. We clamp/threshold/enum-validate/truncate in app code after parsing.


class LLMSignals(BaseModel):
    price_sens: float = 0.0
    loyalty: float = 0.0
    recency: float = 0.0
    novelty: float = 0.0
    engage: float = 0.0
    is_new: float = 0.0                   # model emits a score; we threshold to bool


class LLMFeatureCard(BaseModel):
    persona: str
    f: LLMSignals
    tags: list[str] = Field(default_factory=list)


class LLMBrandCard(BaseModel):
    tone: str = "neutral"
    palette: list[str] = Field(default_factory=list)
    restricted_keywords: list[str] = Field(default_factory=list)


class AnalystLLMOut(BaseModel):
    feature_card: LLMFeatureCard
    brand_card: LLMBrandCard


class LLMSuggestion(BaseModel):
    strategy_id: str                      # plain str -> invalid ids are dropped, not rejected
    title: str
    rationale: str
    target_signal: str = ""


class StrategistLLMOut(BaseModel):
    suggestions: list[LLMSuggestion]


class MarkdownOut(BaseModel):
    markdown: str


class SpecFile(BaseModel):
    name: str
    mime: str
    content: str


# ---- HTTP request bodies ----------------------------------------------------


class AnalyzeReq(BaseModel):
    document_id: str


class RefineReq(BaseModel):
    analysis_id: str
    feedback: str = Field(max_length=2000)


class FeedbackReq(BaseModel):
    strategy_id: StrategyId
    action: Literal["approve", "reject"]


class GenerateSpecsReq(BaseModel):
    analysis_id: str
    approved_ids: list[str] = Field(default_factory=list)


# ---- HTTP responses ---------------------------------------------------------


class UploadResp(BaseModel):
    document_id: str


class AnalyzeResp(BaseModel):
    analysis_id: str


class RefineResp(BaseModel):
    analysis_id: str
    iteration: int


class SpecResp(BaseModel):
    spec_id: str
    files: list[SpecFile]
