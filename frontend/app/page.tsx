"use client";

import { useCallback, useState } from "react";
import {
  analyze,
  ApiError,
  generateSpecs,
  refine,
  sendFeedback,
  uploadFile,
  uploadText,
  type Suggestion,
  type SpecFileMeta,
} from "@/lib/api";
import { useEvents, type AppEvent } from "@/lib/useEvents";
import { TopNav } from "@/components/TopNav";
import { Uploader, type UploadPayload } from "@/components/Uploader";
import { Reasoning, type Stage } from "@/components/Reasoning";
import { SuggestionList } from "@/components/SuggestionList";
import { SpecDownloads } from "@/components/SpecDownloads";

type Phase = "upload" | "reasoning" | "suggestions" | "specs";

export default function Home() {
  const [phase, setPhase] = useState<Phase>("upload");
  const [analysisId, setAnalysisId] = useState<string | null>(null);

  const [stage, setStage] = useState<Stage>("analyzing");
  const [persona, setPersona] = useState<string | undefined>();

  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [iteration, setIteration] = useState(0);
  const [approved, setApproved] = useState<Set<string>>(new Set());
  const [discarded, setDiscarded] = useState<Set<string>>(new Set());

  const [specId, setSpecId] = useState<string | null>(null);
  const [files, setFiles] = useState<SpecFileMeta[]>([]);

  const [busy, setBusy] = useState(false);
  const [refining, setRefining] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [events, setEvents] = useState<AppEvent[]>([]);

  const onEvent = useCallback((ev: AppEvent) => {
    setEvents((prev) => [...prev, ev]);
    const data = ev.data ?? {};
    switch (ev.type) {
      case "analysis.started":
        setStage("analyzing");
        break;
      case "analysis.done":
        setStage("strategizing");
        if (typeof data.persona === "string") setPersona(data.persona);
        break;
      case "suggestions.ready":
        setSuggestions((data.items as Suggestion[]) ?? []);
        if (typeof data.iteration === "number") setIteration(data.iteration);
        setRefining(false);
        setPhase((p) => (p === "specs" ? p : "suggestions"));
        break;
      case "spec.generated":
        if (typeof data.spec_id === "string") setSpecId(data.spec_id);
        if (Array.isArray(data.files)) setFiles(data.files as SpecFileMeta[]);
        setGenerating(false);
        setPhase("specs");
        break;
      case "error":
        setError(ev.msg || "Something went wrong");
        setRefining(false);
        setGenerating(false);
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
      setStage("analyzing");
      setPhase("reasoning");
    } catch (e) {
      const msg = e instanceof ApiError ? `${e.message} (${e.status})` : "Upload failed";
      setError(msg);
    } finally {
      setBusy(false);
    }
  }

  function handleApprove(s: Suggestion) {
    setApproved((prev) => new Set(prev).add(s.strategy_id));
    setDiscarded((prev) => {
      const next = new Set(prev);
      next.delete(s.strategy_id);
      return next;
    });
    sendFeedback(s.strategy_id, "approve").catch(() => {});
  }

  function handleDiscard(s: Suggestion) {
    setDiscarded((prev) => new Set(prev).add(s.strategy_id));
    setApproved((prev) => {
      const next = new Set(prev);
      next.delete(s.strategy_id);
      return next;
    });
    sendFeedback(s.strategy_id, "reject").catch(() => {});
  }

  async function handleRefine(feedback: string) {
    if (!analysisId) return;
    setRefining(true);
    setError(null);
    try {
      await refine(analysisId, feedback);
      // suggestions.ready event will update the list + clear refining.
    } catch (e) {
      setRefining(false);
      setError(
        e instanceof ApiError
          ? e.status === 409
            ? "Refine limit reached (3)."
            : e.message
          : "Refine failed",
      );
    }
  }

  async function handleGenerate() {
    if (!analysisId) return;
    setGenerating(true);
    setError(null);
    const ids = [...approved].filter((id) => !discarded.has(id));
    try {
      const res = await generateSpecs(analysisId, ids);
      // Event-driven transition is primary; use the response as a fallback.
      setSpecId(res.spec_id);
      setFiles(res.files);
      setPhase("specs");
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Spec generation failed");
    } finally {
      setGenerating(false);
    }
  }

  function handleStartOver() {
    setPhase("upload");
    setAnalysisId(null);
    setSuggestions([]);
    setIteration(0);
    setApproved(new Set());
    setDiscarded(new Set());
    setSpecId(null);
    setFiles([]);
    setError(null);
    setPersona(undefined);
  }

  return (
    <>
      <TopNav onStartOver={phase === "upload" ? undefined : handleStartOver} />

      {phase === "upload" && (
        <Uploader onSubmit={handleSubmit} busy={busy} error={error} />
      )}

      {phase === "reasoning" && (
        <Reasoning stage={stage} persona={persona} events={events} />
      )}

      {phase === "suggestions" && (
        <SuggestionList
          suggestions={suggestions}
          iteration={iteration}
          approved={approved}
          discarded={discarded}
          persona={persona}
          refining={refining}
          generating={generating}
          onApprove={handleApprove}
          onDiscard={handleDiscard}
          onRefine={handleRefine}
          onGenerate={handleGenerate}
        />
      )}

      {phase === "specs" && specId && <SpecDownloads specId={specId} files={files} />}

      {/* connection + error toasts */}
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
