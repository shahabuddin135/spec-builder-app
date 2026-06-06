"""Pydantic schemas for the spec generator + reviewer.

Flow: brief -> ProjectBrief (parsed) -> Question[] (clarify) -> ProjectSpec
(enriched, after answers) -> SpecFile[] (rendered package) -> specs.zip.

Agent-facing models are tolerant (plain types, defaults, no enums/limits) so the
provider never rejects the model's own output; we normalize in app code.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

# ---- Parsed understanding of the brief --------------------------------------


class ProjectBrief(BaseModel):
    title: str = "Untitled Project"
    summary: str = ""
    project_type: str = "web app"          # web app | api | cli | mobile | ...
    goals: list[str] = Field(default_factory=list)
    non_goals: list[str] = Field(default_factory=list)
    users: list[str] = Field(default_factory=list)
    features: list[str] = Field(default_factory=list)
    tech: list[str] = Field(default_factory=list)
    open_areas: list[str] = Field(default_factory=list)  # what's vague -> drives questions


class Question(BaseModel):
    id: str
    question: str
    why: str = ""
    suggestions: list[str] = Field(default_factory=list)


class QuestionsOut(BaseModel):
    questions: list[Question] = Field(default_factory=list)


# ---- Enriched, render-ready spec --------------------------------------------


class Entity(BaseModel):
    name: str
    fields: list[str] = Field(default_factory=list)


class Endpoint(BaseModel):
    method: str = "GET"
    path: str = "/"
    purpose: str = ""


class Phase(BaseModel):
    name: str
    tasks: list[str] = Field(default_factory=list)


class ProjectSpec(BaseModel):
    title: str = "Untitled Project"
    summary: str = ""
    project_type: str = "web app"
    goal: str = ""
    non_goals: list[str] = Field(default_factory=list)
    users: list[str] = Field(default_factory=list)
    features: list[str] = Field(default_factory=list)
    entities: list[Entity] = Field(default_factory=list)
    backend_modules: list[str] = Field(default_factory=list)
    backend_endpoints: list[Endpoint] = Field(default_factory=list)
    frontend_screens: list[str] = Field(default_factory=list)
    frontend_state: list[str] = Field(default_factory=list)
    tech: list[str] = Field(default_factory=list)
    scale: list[str] = Field(default_factory=list)
    hard_rules: list[str] = Field(default_factory=list)
    security: list[str] = Field(default_factory=list)
    phases: list[Phase] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)


# ---- Rendered output --------------------------------------------------------


class SpecFile(BaseModel):
    path: str            # e.g. "backend_specs/ARCH.md"
    mime: str = "text/markdown"
    content: str


class SpecFileMeta(BaseModel):
    path: str
    mime: str = "text/markdown"


# ---- HTTP request bodies ----------------------------------------------------


class AnalyzeReq(BaseModel):
    document_id: str


class AnswerItem(BaseModel):
    id: str
    answer: str = ""


class GenerateReq(BaseModel):
    analysis_id: str
    answers: list[AnswerItem] = Field(default_factory=list)


class RefineReq(BaseModel):
    analysis_id: str
    feedback: str = Field(default="", max_length=2000)


# ---- HTTP responses ---------------------------------------------------------


class UploadResp(BaseModel):
    document_id: str


class AnalyzeResp(BaseModel):
    analysis_id: str


class GenerateResp(BaseModel):
    spec_id: str


class SpecResp(BaseModel):
    spec_id: str
    iteration: int
    files: list[SpecFileMeta]
