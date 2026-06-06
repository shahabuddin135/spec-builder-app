"use client";

import { useState } from "react";
import type { Suggestion } from "@/lib/api";

export function SuggestionList({
  suggestions,
  iteration,
  approved,
  discarded,
  persona,
  refining,
  generating,
  onApprove,
  onDiscard,
  onRefine,
  onGenerate,
}: {
  suggestions: Suggestion[];
  iteration: number;
  approved: Set<string>;
  discarded: Set<string>;
  persona?: string;
  refining: boolean;
  generating: boolean;
  onApprove: (s: Suggestion) => void;
  onDiscard: (s: Suggestion) => void;
  onRefine: (feedback: string) => void;
  onGenerate: () => void;
}) {
  const [feedback, setFeedback] = useState("");
  const maxedRefine = iteration >= 3;
  const visible = suggestions.filter((s) => !discarded.has(s.strategy_id));
  const approvedCount = visible.filter((s) => approved.has(s.strategy_id)).length;

  return (
    <main className="mx-auto flex max-w-[720px] flex-col gap-6 px-4 pb-32 pt-20 sm:px-6">
      <header className="flex flex-col gap-1">
        <div className="flex items-center justify-between">
          <h1 className="text-headline-lg text-primary">Strategy suggestions</h1>
          <span className="text-label-md uppercase tracking-widest text-on-surface-variant">
            Iteration {iteration} · {visible.length} ranked
          </span>
        </div>
        <p className="text-body-md text-on-surface-variant">
          {persona ? `Persona: ${persona}. ` : ""}Approve the ones you want, discard the
          rest, then generate spec files. Feedback tunes future rankings.
        </p>
      </header>

      <div className="flex flex-col gap-3">
        {visible.map((s, i) => {
          const isApproved = approved.has(s.strategy_id);
          return (
            <div
              key={s.strategy_id}
              className={`rounded-lg border p-4 transition-all ${
                isApproved
                  ? "border-primary bg-surface-container"
                  : "border-outline-variant bg-surface-container-low"
              }`}
            >
              <div className="flex items-start gap-4">
                <div className="text-code-md mt-0.5 w-6 shrink-0 text-on-surface-variant opacity-60">
                  {String(i + 1).padStart(2, "0")}
                </div>
                <div className="flex-1">
                  <div className="mb-1 flex flex-wrap items-center gap-2">
                    <span className="text-body-md font-bold text-primary">{s.title}</span>
                    <span className="text-code-md rounded bg-surface-container-highest px-2 py-0.5 text-[11px] text-on-surface-variant">
                      {s.strategy_id}
                    </span>
                    {s.on_brand ? (
                      <span className="flex items-center gap-1 text-[11px] text-secondary">
                        <span
                          className="material-symbols-outlined text-[14px]"
                          style={{ fontVariationSettings: "'FILL' 1" }}
                        >
                          check_circle
                        </span>
                        on-brand
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 text-[11px] text-error">
                        <span className="material-symbols-outlined text-[14px]">warning</span>
                        review
                      </span>
                    )}
                  </div>
                  <p className="text-body-md text-on-surface-variant">{s.rationale}</p>
                  <p className="text-label-md mt-1 uppercase tracking-widest text-on-surface-variant opacity-60">
                    Targets {s.target_signal}
                  </p>
                </div>
                <div className="flex shrink-0 flex-col gap-2">
                  <button
                    onClick={() => onApprove(s)}
                    className={`flex h-8 w-8 items-center justify-center rounded transition-colors ${
                      isApproved
                        ? "bg-primary text-surface-dim"
                        : "bg-surface-container-highest text-on-surface-variant hover:text-primary"
                    }`}
                    aria-label="Approve"
                    title="Approve"
                  >
                    <span className="material-symbols-outlined text-[18px]">check</span>
                  </button>
                  <button
                    onClick={() => onDiscard(s)}
                    className="flex h-8 w-8 items-center justify-center rounded bg-surface-container-highest text-on-surface-variant transition-colors hover:text-error"
                    aria-label="Discard"
                    title="Discard"
                  >
                    <span className="material-symbols-outlined text-[18px]">close</span>
                  </button>
                </div>
              </div>
            </div>
          );
        })}
        {visible.length === 0 && (
          <p className="text-body-md py-8 text-center text-on-surface-variant">
            All suggestions discarded. Refine below to get new ones.
          </p>
        )}
      </div>

      {/* Refine */}
      <div className="rounded-xl border border-dashed border-outline-variant bg-surface-container-lowest p-4">
        <label className="text-label-md mb-2 block uppercase tracking-widest text-on-surface-variant">
          Refine {maxedRefine && "· limit reached (3)"}
        </label>
        <div className="flex flex-col gap-2 sm:flex-row">
          <input
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            disabled={refining || maxedRefine}
            placeholder="e.g. lean into loyalty and new-customer plays"
            className="text-body-md flex-1 rounded-lg border border-outline bg-surface-container-low px-3 py-2 text-primary placeholder-[#555555] focus:border-outline-variant focus:outline-none disabled:opacity-50"
          />
          <button
            onClick={() => {
              if (feedback.trim()) {
                onRefine(feedback.trim());
                setFeedback("");
              }
            }}
            disabled={refining || maxedRefine || feedback.trim().length === 0}
            className="flex items-center justify-center gap-1 rounded-lg border border-outline bg-surface-container-high px-4 py-2 text-on-surface transition-colors hover:text-primary disabled:cursor-not-allowed disabled:opacity-40"
          >
            <span className="material-symbols-outlined text-[18px]">refresh</span>
            {refining ? "Refining…" : "Refine"}
          </button>
        </div>
      </div>

      {/* Sticky generate bar */}
      <div className="fixed inset-x-0 bottom-0 border-t border-outline bg-surface-container-low/95 backdrop-blur">
        <div className="mx-auto flex max-w-[720px] items-center justify-between px-4 py-3 sm:px-6">
          <span className="text-label-md text-on-surface-variant">
            {approvedCount > 0
              ? `${approvedCount} approved`
              : "None approved — all will be included"}
          </span>
          <button
            onClick={onGenerate}
            disabled={generating || visible.length === 0}
            className="flex items-center gap-2 rounded-lg bg-primary px-6 py-3 font-bold text-background transition-all hover:opacity-90 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-40"
          >
            {generating ? "Generating…" : "Generate specs"}
            {!generating && (
              <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
            )}
          </button>
        </div>
      </div>
    </main>
  );
}
