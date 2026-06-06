# CONTEXT — Goal & Scope

> What this product is and what it is not. Immutable unless explicitly changed.

## Goal

**SpecForge turns a vague project brief into a clear, reviewed specification package.**
A user uploads or pastes a rough idea; a small network of agents parses it, **asks
clarifying questions** about what they want to achieve, generates a complete structured
spec (clean markdown), lets the user **review and request changes**, and produces a
downloadable **`specs.zip`**.

## Primary users

- Builders / founders / PMs who have an app idea but not a written spec.
- Engineers who want a consistent starting structure for a new project.

## In scope

- Upload `.txt` / `.md` brief (or paste text).
- Parse the brief into a structured understanding.
- Generate clarifying questions and collect answers.
- Produce a full spec package: `SPEC.md`, `CONTEXT.md`, `CONSTRAINTS.md`, `SECURITY.md`,
  `MEMORY.md`, `backend_specs/{ARCH,CONTRACT,PLAN,tasks}`, `frontend_specs/{ARCH,CONTRACT,PLAN,tasks}`, `README.md`.
- Free-text "request changes" to regenerate.
- Download individual files or the whole `specs.zip`.

## Non-goals

- No authentication / accounts (prototype).
- Generating the actual application code (we produce the spec, not the build).
- PDF/docx ingestion — `.txt` / `.md` only.
- Real-time collaboration / multi-user projects.
