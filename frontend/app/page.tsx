"use client";

import { useCallback, useState } from "react";
import {
  analyze,
  ApiError,
  generateSpecs,
  refine,
  uploadFile,
  uploadText,
  type Answer,
  type Question,
  type SpecFileMeta,
} from "@/lib/api";
import { useEvents, type AppEvent } from "@/lib/useEvents";
import { TopNav } from "@/components/TopNav";
import { Uploader, type UploadPayload } from "@/components/Uploader";
import { Reasoning, type Step } from "@/components/Reasoning";
import { QuestionForm } from "@/components/QuestionForm";
import { SpecReview } from "@/components/SpecReview";

type Phase = "upload" | "parsing" | "clarify" | "generating" | "review";

const ICONS = { analyst: "data_object", clarifier: "quiz", writer: "edit_note" };

export default function Home() {
  const [phase, setPhase] = useState<Phase>("upload");
  const [analysisId, setAnalysisId] = useState<string | null>(null);
  const [title, setTitle] = useState("");
  const [parseStage, setParseStage] = useState<"analyzing" | "clarifying">("analyzing");

  const [questions, setQuestions] = useState<Question[]>([]);
  const [specId, setSpecId] = useState<string | null>(null);
  const [files, setFiles] = useState<SpecFileMeta[]>([]);
  const [iteration, setIteration] = useState(0);

  const [busy, setBusy] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [refining, setRefining] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [events, setEvents] = useState<AppEvent[]>([]);

  const onEvent = useCallback((ev: AppEvent) => {
    setEvents((prev) => [...prev, ev]);
    const data = ev.data ?? {};
    switch (ev.type) {
      case "analysis.started":
        setParseStage("analyzing");
        break;
      case "analysis.done":
        setParseStage("clarifying");
        if (typeof data.title === "string") setTitle(data.title);
        break;
      case "questions.ready":
        setQuestions((data.questions as Question[]) ?? []);
        setPhase("clarify");
        break;
      case "spec.generating":
        setPhase((p) => (p === "review" ? p : "generating"));
        break;
      case "spec.generated":
        if (typeof data.spec_id === "string") setSpecId(data.spec_id);
        if (Array.isArray(data.files)) setFiles(data.files as SpecFileMeta[]);
        if (typeof data.iteration === "number") setIteration(data.iteration);
        if (typeof data.title === "string" && data.title) setTitle(data.title);
        setGenerating(false);
        setRefining(false);
        setPhase("review");
        break;
      case "error":
        setError(ev.msg || "Something went wrong");
        setGenerating(false);
        setRefining(false);
        break;
    }
  }, []);

  const { connected } = useEvents(onEvent);

  async function handleSubmit(payload: UploadPayload) {
    setBusy(true);
    setError(null);
    try {
      const { document_id } = payload.file
        ? await uploadFile(payload.file)
        : await uploadText(payload.text ?? "");
      const { analysis_id } = await analyze(document_id);
      setAnalysisId(analysis_id);
      setParseStage("analyzing");
      setPhase("parsing");
    } catch (e) {
      setError(e instanceof ApiError ? `${e.message} (${e.status})` : "Upload failed");
    } finally {
      setBusy(false);
    }
  }

  async function handleAnswers(answers: Answer[]) {
    if (!analysisId) return;
    setGenerating(true);
    setError(null);
    setPhase("generating");
    try {
      await generateSpecs(analysisId, answers);
    } catch (e) {
      setGenerating(false);
      setPhase("clarify");
      setError(e instanceof ApiError ? e.message : "Generation failed");
    }
  }

  async function handleRefine(feedback: string) {
    if (!analysisId) return;
    setRefining(true);
    setError(null);
    try {
      await refine(analysisId, feedback);
    } catch (e) {
      setRefining(false);
      setError(
        e instanceof ApiError
          ? e.status === 409
            ? "Revision limit reached."
            : e.message
          : "Refine failed",
      );
    }
  }

  function handleStartOver() {
    setPhase("upload");
    setAnalysisId(null);
    setTitle("");
    setQuestions([]);
    setSpecId(null);
    setFiles([]);
    setIteration(0);
    setError(null);
  }

  function parsingSteps(): Step[] {
    const analyzing = parseStage === "analyzing";
    return [
      {
        label: "Analyst",
        icon: ICONS.analyst,
        state: analyzing ? "active" : "done",
        detail: analyzing ? "Reading the brief and extracting structure…" : "Brief parsed.",
      },
      {
        label: "Clarifier",
        icon: ICONS.clarifier,
        state: analyzing ? "pending" : "active",
        detail: analyzing ? "Waiting…" : "Working out what to ask you…",
      },
      { label: "Spec-Writer", icon: ICONS.writer, state: "pending", detail: "Waiting…" },
    ];
  }

  function generatingSteps(): Step[] {
    return [
      { label: "Analyst", icon: ICONS.analyst, state: "done", detail: "Brief parsed." },
      { label: "Clarifier", icon: ICONS.clarifier, state: "done", detail: "Answers captured." },
      {
        label: "Spec-Writer",
        icon: ICONS.writer,
        state: "active",
        detail: "Assembling the full spec package…",
      },
    ];
  }

  return (
    <>
      <TopNav onStartOver={phase === "upload" ? undefined : handleStartOver} />

      {phase === "upload" && <Uploader onSubmit={handleSubmit} busy={busy} error={error} />}

      {phase === "parsing" && (
        <Reasoning
          title="Analyzing your brief"
          subtitle="Turning a vague idea into a precise spec"
          steps={parsingSteps()}
          events={events}
        />
      )}

      {phase === "clarify" && (
        <QuestionForm
          title={title}
          questions={questions}
          busy={generating}
          onSubmit={handleAnswers}
        />
      )}

      {phase === "generating" && (
        <Reasoning
          title="Writing your spec package"
          subtitle="Spec-Writer assembling the files"
          steps={generatingSteps()}
          events={events}
        />
      )}

      {phase === "review" && specId && (
        <SpecReview
          specId={specId}
          files={files}
          title={title}
          iteration={iteration}
          refining={refining}
          onRefine={handleRefine}
        />
      )}

      {!connected && phase !== "upload" && (
        <div className="fixed bottom-4 left-4 z-50 flex items-center gap-2 rounded-lg border border-outline bg-surface-container px-3 py-2 text-label-md text-on-surface-variant">
          <span className="h-1.5 w-1.5 rounded-full bg-error" />
          Reconnecting to event stream…
        </div>
      )}
      {error && phase !== "upload" && (
        <div className="fixed bottom-4 right-4 z-50 max-w-sm rounded-lg border border-error/40 bg-error-container/30 px-4 py-2 text-label-md text-on-error-container">
          {error}
        </div>
      )}
    </>
  );
}
