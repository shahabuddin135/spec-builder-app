"use client";

import { useState } from "react";
import { fileUrl, zipUrl, type SpecFileMeta } from "@/lib/api";

const ICON: Record<string, string> = {
  "text/markdown": "description",
  "application/json": "data_object",
};

function groupByFolder(files: SpecFileMeta[]): [string, SpecFileMeta[]][] {
  const groups = new Map<string, SpecFileMeta[]>();
  for (const f of files) {
    const slash = f.path.indexOf("/");
    const key = slash === -1 ? "root" : f.path.slice(0, f.path.lastIndexOf("/"));
    (groups.get(key) ?? groups.set(key, []).get(key)!).push(f);
  }
  return [...groups.entries()];
}

export function SpecReview({
  specId,
  files,
  title,
  iteration,
  refining,
  onRefine,
}: {
  specId: string;
  files: SpecFileMeta[];
  title: string;
  iteration: number;
  refining: boolean;
  onRefine: (feedback: string) => void;
}) {
  const [open, setOpen] = useState<string | null>(null);
  const [cache, setCache] = useState<Record<string, string>>({});
  const [feedback, setFeedback] = useState("");

  async function toggle(path: string) {
    if (open === path) {
      setOpen(null);
      return;
    }
    setOpen(path);
    if (cache[path] === undefined) {
      try {
        const text = await fetch(fileUrl(specId, path)).then((r) => r.text());
        setCache((prev) => ({ ...prev, [path]: text }));
      } catch {
        setCache((prev) => ({ ...prev, [path]: "// failed to load preview" }));
      }
    }
  }

  return (
    <main className="mx-auto flex max-w-[760px] flex-col gap-6 px-4 pb-40 pt-20 sm:px-6">
      <header className="flex flex-col items-center gap-3 text-center">
        <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-outline bg-surface-container-high">
          <span className="material-symbols-outlined text-[28px] text-primary">task_alt</span>
        </div>
        <h1 className="text-headline-lg text-primary">Your spec package is ready</h1>
        <p className="text-body-md text-on-surface-variant">
          {title ? `“${title}” — ` : ""}
          {files.length} files
          {iteration > 0 ? ` · revision ${iteration}` : ""}. Review below, request changes, or
          download.
        </p>
        <a
          href={zipUrl(specId)}
          className="group mt-2 flex h-[64px] w-full max-w-[360px] items-center justify-center gap-3 rounded-[10px] bg-[#f2f2f2] font-bold text-[#1a1a1a] transition-all hover:opacity-95 active:scale-[0.98]"
        >
          <span className="material-symbols-outlined text-[28px] transition-transform group-hover:-translate-y-0.5">
            download
          </span>
          Download specs.zip
        </a>
      </header>

      {/* File tree with inline preview */}
      <div className="flex flex-col gap-5">
        {groupByFolder(files).map(([folder, group]) => (
          <div key={folder} className="flex flex-col gap-1.5">
            <h3 className="text-label-md uppercase tracking-widest text-on-surface-variant opacity-70">
              {folder === "root" ? "/" : `${folder}/`}
            </h3>
            {group.map((f) => {
              const name = f.path.split("/").pop();
              const isOpen = open === f.path;
              return (
                <div
                  key={f.path}
                  className="overflow-hidden rounded-lg border border-outline-variant bg-surface-container-low"
                >
                  <div className="flex items-center justify-between px-4 py-2.5">
                    <button
                      onClick={() => toggle(f.path)}
                      className="flex flex-1 items-center gap-2 text-left"
                    >
                      <span className="material-symbols-outlined text-[18px] text-on-surface-variant">
                        {ICON[f.mime] ?? "draft"}
                      </span>
                      <span className="text-code-md text-primary">{name}</span>
                      <span className="material-symbols-outlined text-[16px] text-on-surface-variant opacity-60">
                        {isOpen ? "expand_less" : "expand_more"}
                      </span>
                    </button>
                    <a
                      href={fileUrl(specId, f.path)}
                      className="flex items-center text-on-surface-variant transition-colors hover:text-primary"
                      aria-label={`Download ${name}`}
                    >
                      <span className="material-symbols-outlined text-[18px]">download</span>
                    </a>
                  </div>
                  {isOpen && (
                    <pre className="scroll-slim max-h-80 overflow-auto border-t border-outline-variant bg-surface-container-lowest p-4 text-code-md text-on-surface">
                      {cache[f.path] ?? "Loading…"}
                    </pre>
                  )}
                </div>
              );
            })}
          </div>
        ))}
      </div>

      {/* Request changes */}
      <div className="fixed inset-x-0 bottom-0 border-t border-outline bg-surface-container-low/95 backdrop-blur">
        <div className="mx-auto flex max-w-[760px] flex-col gap-2 px-4 py-3 sm:flex-row sm:px-6">
          <input
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            disabled={refining}
            placeholder="Request changes, e.g. “add an export-to-CSV feature” or “use SQLite”"
            className="text-body-md flex-1 rounded-lg border border-outline bg-surface-container px-3 py-2 text-primary placeholder-[#555555] focus:border-outline-variant focus:outline-none disabled:opacity-50"
          />
          <button
            onClick={() => {
              if (feedback.trim()) {
                onRefine(feedback.trim());
                setFeedback("");
              }
            }}
            disabled={refining || feedback.trim().length === 0}
            className="flex items-center justify-center gap-1 rounded-lg border border-outline bg-surface-container-high px-4 py-2 text-on-surface transition-colors hover:text-primary disabled:cursor-not-allowed disabled:opacity-40"
          >
            <span className="material-symbols-outlined text-[18px]">refresh</span>
            {refining ? "Regenerating…" : "Request changes"}
          </button>
        </div>
      </div>
    </main>
  );
}
