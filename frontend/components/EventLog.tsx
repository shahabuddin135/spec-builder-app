"use client";

import type { AppEvent } from "@/lib/useEvents";

function timeOf(ts: string): string {
  const d = new Date(ts);
  return Number.isNaN(d.getTime()) ? "" : d.toLocaleTimeString();
}

export function EventLog({ events }: { events: AppEvent[] }) {
  return (
    <div className="rounded-xl border border-dashed border-outline-variant bg-surface-container-lowest p-6">
      <div className="mb-4 flex items-center gap-2">
        <span className="material-symbols-outlined text-[18px] text-primary">forum</span>
        <h3 className="text-label-md uppercase tracking-widest text-on-surface-variant">
          Live event feed
        </h3>
      </div>
      <div className="scroll-slim flex max-h-48 flex-col gap-2 overflow-y-auto">
        {events.length === 0 && (
          <p className="text-code-md text-on-surface-variant opacity-50">
            Waiting for events…
          </p>
        )}
        {events.map((ev, i) => (
          <div key={i} className="flex items-baseline justify-between gap-4">
            <span className="text-code-md text-on-surface">
              <span className="text-on-surface-variant opacity-60">{ev.type}</span>{" "}
              — {ev.msg}
            </span>
            <span className="text-code-md shrink-0 text-on-surface-variant opacity-50">
              {timeOf(ev.ts)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
