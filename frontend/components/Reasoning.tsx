"use client";

import type { AppEvent } from "@/lib/useEvents";
import { EventLog } from "./EventLog";

export interface Step {
  label: string;
  icon: string;
  state: "done" | "active" | "pending";
  detail?: string;
}

export function Reasoning({
  title,
  subtitle,
  steps,
  events,
}: {
  title: string;
  subtitle: string;
  steps: Step[];
  events: AppEvent[];
}) {
  return (
    <main className="mx-auto flex max-w-[640px] flex-col items-center px-4 pb-16 pt-20 sm:px-0">
      <div className="mb-8 text-center">
        <h1 className="text-headline-lg text-primary">{title}</h1>
        <p className="text-label-md mt-1 uppercase tracking-widest text-on-surface-variant">
          {subtitle}
        </p>
      </div>

      {/* Step indicator */}
      <div className="relative mb-10 flex w-full items-start justify-between px-6">
        <div className="absolute left-0 top-4 -z-10 h-px w-full bg-outline-variant" />
        {steps.map((step) => (
          <div
            key={step.label}
            className={`flex flex-col items-center gap-1 bg-background px-2 ${
              step.state === "pending" ? "opacity-40" : ""
            }`}
          >
            <div
              className={
                step.state === "done"
                  ? "flex h-8 w-8 items-center justify-center rounded-full bg-primary text-surface-dim"
                  : step.state === "active"
                    ? "relative flex h-8 w-8 items-center justify-center rounded-full border-2 border-dashed border-primary"
                    : "flex h-8 w-8 items-center justify-center rounded-full border border-outline"
              }
            >
              {step.state === "done" ? (
                <span className="material-symbols-outlined text-[18px]">check</span>
              ) : step.state === "active" ? (
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
                step.state === "active" ? "font-bold text-primary" : "text-on-surface-variant"
              }`}
            >
              {step.label}
            </span>
          </div>
        ))}
      </div>

      {/* Agent cards */}
      <div className="mb-8 w-full space-y-4">
        {steps.map((step) => {
          const active = step.state === "active";
          const status =
            step.state === "done" ? "COMPLETED" : active ? "PROCESSING" : "WAITING";
          return (
            <div
              key={step.label}
              className={`flex items-center gap-4 rounded-lg p-4 ${
                active
                  ? "border-2 border-dashed border-primary bg-surface-container"
                  : "border border-outline-variant bg-surface-container-low"
              } ${step.state === "pending" ? "opacity-40" : ""}`}
            >
              <div
                className={`flex h-10 w-10 items-center justify-center rounded ${
                  active
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
                      step.state === "pending" ? "text-on-surface-variant" : "text-primary"
                    }`}
                  >
                    {step.label}
                  </span>
                  <span className="flex items-center gap-1.5">
                    {active && (
                      <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-primary" />
                    )}
                    <span className="text-label-md text-on-surface-variant">{status}</span>
                  </span>
                </div>
                <p className={`text-body-md ${active ? "text-primary" : "text-on-surface-variant"}`}>
                  {step.detail ?? (active ? "Working…" : status === "COMPLETED" ? "Done." : "Waiting…")}
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
