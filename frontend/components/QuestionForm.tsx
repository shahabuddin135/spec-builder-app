"use client";

import { useState } from "react";
import type { Answer, Question } from "@/lib/api";

export function QuestionForm({
  title,
  questions,
  busy,
  onSubmit,
}: {
  title: string;
  questions: Question[];
  busy: boolean;
  onSubmit: (answers: Answer[]) => void;
}) {
  const [values, setValues] = useState<Record<string, string>>({});

  function set(id: string, v: string) {
    setValues((prev) => ({ ...prev, [id]: v }));
  }

  function submit() {
    const answers = questions.map((q) => ({ id: q.id, answer: (values[q.id] ?? "").trim() }));
    onSubmit(answers);
  }

  const answeredCount = questions.filter((q) => (values[q.id] ?? "").trim()).length;

  return (
    <main className="mx-auto flex max-w-[640px] flex-col gap-6 px-4 pb-32 pt-20 sm:px-0">
      <header className="flex flex-col gap-1">
        <div className="flex items-center justify-between">
          <h1 className="text-headline-lg text-primary">A few questions</h1>
          <span className="text-label-md uppercase tracking-widest text-on-surface-variant">
            {answeredCount}/{questions.length} answered
          </span>
        </div>
        <p className="text-body-md text-on-surface-variant">
          {title ? `For “${title}”. ` : ""}Answer what you can — anything left blank gets a
          sensible default. This is how a vague brief becomes a precise spec.
        </p>
      </header>

      <div className="flex flex-col gap-4">
        {questions.map((q, i) => (
          <div
            key={q.id}
            className="rounded-lg border border-outline-variant bg-surface-container-low p-4"
          >
            <div className="mb-1 flex items-baseline gap-2">
              <span className="text-code-md text-on-surface-variant opacity-60">
                {String(i + 1).padStart(2, "0")}
              </span>
              <h2 className="text-body-md font-bold text-primary">{q.question}</h2>
            </div>
            {q.why && (
              <p className="text-label-md mb-2 pl-6 text-on-surface-variant opacity-70">
                {q.why}
              </p>
            )}
            {q.suggestions.length > 0 && (
              <div className="mb-2 flex flex-wrap gap-2 pl-6">
                {q.suggestions.map((s) => (
                  <button
                    key={s}
                    type="button"
                    onClick={() =>
                      set(q.id, values[q.id] ? `${values[q.id]}, ${s}` : s)
                    }
                    className="text-label-md rounded-full border border-outline bg-surface-container px-3 py-1 text-on-surface-variant transition-colors hover:border-outline-variant hover:text-primary"
                  >
                    + {s}
                  </button>
                ))}
              </div>
            )}
            <textarea
              value={values[q.id] ?? ""}
              onChange={(e) => set(q.id, e.target.value)}
              disabled={busy}
              rows={2}
              placeholder="Your answer (optional)…"
              className="text-body-md ml-6 w-[calc(100%-1.5rem)] resize-none rounded-lg border border-outline bg-surface-container-low p-3 text-primary placeholder-[#555555] focus:border-outline-variant focus:outline-none disabled:opacity-50"
            />
          </div>
        ))}
      </div>

      {/* Sticky action bar */}
      <div className="fixed inset-x-0 bottom-0 border-t border-outline bg-surface-container-low/95 backdrop-blur">
        <div className="mx-auto flex max-w-[640px] items-center justify-between px-4 py-3 sm:px-0">
          <span className="text-label-md text-on-surface-variant">
            Turning your brief into a full spec package
          </span>
          <button
            onClick={submit}
            disabled={busy}
            className="flex items-center gap-2 rounded-lg bg-primary px-6 py-3 font-bold text-background transition-all hover:opacity-90 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-40"
          >
            {busy ? "Generating…" : "Generate spec package"}
            {!busy && <span className="material-symbols-outlined text-[18px]">arrow_forward</span>}
          </button>
        </div>
      </div>
    </main>
  );
}
