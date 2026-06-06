"use client";

import type { AppEvent } from "@/lib/useEvents";
import { EventLog } from "./EventLog";

export type Stage = "analyzing" | "strategizing";

interface StepDef {
  key: string;
  label: string;
  icon: string;
}

const STEPS: StepDef[] = [
  { key: "analyze", label: "Analyst", icon: "data_object" },
  { key: "strategize", label: "Strategist", icon: "psychology" },
  { key: "write", label: "Spec-Writer", icon: "edit_note" },
];

// 0 = analyzing, 1 = strategizing, 2 = writing (writing happens after approval).
function activeIndex(stage: Stage): number {
  return stage === "analyzing" ? 0 : 1;
}

export function Reasoning({
  stage,
  persona,
  events,
}: {
  stage: Stage;
  persona?: string;
  events: AppEvent[];
}) {
  const active = activeIndex(stage);

  return (
    <main className="mx-auto flex max-w-[640px] flex-col items-center px-4 pb-16 pt-20 sm:px-0">
      <div className="mb-8 text-center">
        <h1 className="text-headline-lg text-primary">Analyzing your requirements</h1>
        <p className="text-label-md mt-1 uppercase tracking-widest text-on-surface-variant">
          3 agents running in sequence
        </p>
      </div>

      {/* Step indicator */}
      <div className="relative mb-10 flex w-full items-start justify-between px-6">
        <div className="absolute left-0 top-4 -z-10 h-px w-full bg-outline-variant" />
        {STEPS.map((step, i) => {
          const done = i < active;
          const isActive = i === active;
          return (
            <div
              key={step.key}
              className={`flex flex-col items-center gap-1 bg-background px-2 ${
                i > active ? "opacity-40" : ""
              }`}
            >
              <div
                className={
                  done
                    ? "flex h-8 w-8 items-center justify-center rounded-full bg-primary text-surface-dim"
                    : isActive
                      ? "relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-dashed border-primary"
                      : "flex h-8 w-8 items-center justify-center rounded-full border border-outline"
                }
              >
                {done ? (
                  <span className="material-symbols-outlined text-[18px]">check</span>
                ) : isActive ? (
                  <>
                    <div className="h-3 w-3 rounded-full bg-primary" />
                    <div className="pulse-effect absolute inset-0 rounded-full border border-primary" />
                  </>
                ) : (
                  <div className="h-2 w-2 rounded-full bg-outline" />
                )}
              </div>
              <span
                className={`text-label-md ${
                  isActive ? "font-bold text-primary" : "text-on-surface-variant"
                }`}
              >
                {step.label}
              </span>
            </div>
          );
        })}
      </div>

      {/* Agent cards */}
      <div className="mb-8 w-full space-y-4">
        {STEPS.map((step, i) => {
          const done = i < active;
          const isActive = i === active;
          const status = done ? "COMPLETED" : isActive ? "PROCESSING" : "WAITING";
          const detail = done
            ? i === 0
              ? `Extracted a compact feature card${persona ? ` · persona “${persona}”` : ""}.`
              : "Done."
            : isActive
              ? i === 0
                ? "Reading the brief as untrusted data and building a feature card…"
                : "Ranking on-brand strategies from the fixed library…"
              : "Waiting…";
          return (
            <div
              key={step.key}
              className={`flex items-center gap-4 rounded-lg p-4 ${
                isActive
                  ? "border-2 border-dashed border-primary bg-surface-container"
                  : "border border-outline-variant bg-surface-container-low"
              } ${i > active ? "opacity-40" : ""}`}
            >
              <div
                className={`flex h-10 w-10 items-center justify-center rounded ${
                  isActive
                    ? "bg-primary text-surface-dim"
                    : "bg-surface-container-highest text-on-surface-variant"
                }`}
              >
                <span className="material-symbols-outlined">{step.icon}</span>
              </div>
              <div className="flex-1">
                <div className="mb-1 flex items-center justify-between">
                  <span
                    className={`text-body-md font-bold ${
                      i <= active ? "text-primary" : "text-on-surface-variant"
                    }`}
                  >
                    {step.label}
                  </span>
                  <span className="flex items-center gap-1.5">
                    {isActive && (
                      <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-primary" />
                    )}
                    <span className="text-label-md text-on-surface-variant">{status}</span>
                  </span>
                </div>
                <p
                  className={`text-body-md ${
                    isActive ? "text-primary" : "text-on-surface-variant"
                  }`}
                >
                  {detail}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      <div className="w-full">
        <EventLog events={events} />
      </div>
    </main>
  );
}
