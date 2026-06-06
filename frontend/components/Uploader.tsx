"use client";

import { useRef, useState } from "react";

export interface UploadPayload {
  text?: string;
  file?: File;
}

const ACCEPT = [".txt", ".md"];

function hasAllowedExt(name: string): boolean {
  return ACCEPT.some((ext) => name.toLowerCase().endsWith(ext));
}

export function Uploader({
  onSubmit,
  busy,
  error,
}: {
  onSubmit: (payload: UploadPayload) => void;
  busy: boolean;
  error: string | null;
}) {
  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const canSubmit = !busy && (!!file || text.trim().length > 5);

  function pickFile(f: File | undefined) {
    if (!f) return;
    if (!hasAllowedExt(f.name)) {
      setLocalError("Only .txt and .md files are accepted.");
      return;
    }
    setLocalError(null);
    setFile(f);
  }

  function submit() {
    if (!canSubmit) return;
    onSubmit(file ? { file } : { text });
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-4 pt-12 sm:px-10">
      <div className="flex w-full max-w-[560px] flex-col items-center">
        {/* Hero */}
        <div className="mb-8 flex flex-col items-center text-center">
          <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-xl border border-outline bg-surface-container-high">
            <span className="material-symbols-outlined text-[32px] text-primary">
              terminal
            </span>
          </div>
          <h1 className="text-headline-lg mb-1 text-primary">
            Turn a rough idea into a full spec
          </h1>
          <p className="text-body-lg text-on-surface-variant">
            Describe your app idea, or upload a .txt / .md brief. We&apos;ll ask a few
            questions, then generate a downloadable spec package.
          </p>
        </div>

        {/* Interaction canvas */}
        <div className="flex w-full flex-col gap-4">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            disabled={busy}
            placeholder="Describe your brand and audience…"
            className="text-body-md h-[140px] w-full resize-none rounded-lg border border-outline bg-surface-container-low p-4 text-primary placeholder-[#555555] transition-all focus:border-outline-variant focus:outline-none disabled:opacity-50"
          />

          {/* Drop zone / file chip */}
          {file ? (
            <div className="flex h-[64px] items-center justify-between rounded-lg border border-outline bg-surface-container-low px-4">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-[20px] text-secondary">
                  description
                </span>
                <span className="text-code-md text-primary">{file.name}</span>
                <span className="text-label-md text-on-surface-variant">
                  {(file.size / 1024).toFixed(1)} KB
                </span>
              </div>
              <button
                onClick={() => setFile(null)}
                disabled={busy}
                className="flex items-center p-1 text-on-surface-variant transition-colors hover:text-error"
                aria-label="Remove file"
              >
                <span className="material-symbols-outlined text-[18px]">close</span>
              </button>
            </div>
          ) : (
            <div
              onClick={() => inputRef.current?.click()}
              onDragOver={(e) => {
                e.preventDefault();
                setDragOver(true);
              }}
              onDragLeave={() => setDragOver(false)}
              onDrop={(e) => {
                e.preventDefault();
                setDragOver(false);
                pickFile(e.dataTransfer.files?.[0]);
              }}
              className={`flex h-[100px] cursor-pointer flex-col items-center justify-center gap-1 rounded-lg border border-dashed transition-colors ${
                dragOver
                  ? "border-primary bg-surface-container-low"
                  : "border-outline hover:bg-surface-container-low"
              }`}
            >
              <span className="material-symbols-outlined text-on-surface-variant">
                upload
              </span>
              <p className="text-label-md text-on-surface-variant">
                Drop a .txt or .md file, or{" "}
                <span className="text-primary underline">click to browse</span>
              </p>
              <input
                ref={inputRef}
                type="file"
                accept=".txt,.md,text/plain,text/markdown"
                className="hidden"
                onChange={(e) => pickFile(e.target.files?.[0])}
              />
            </div>
          )}

          <button
            onClick={submit}
            disabled={!canSubmit}
            className={`flex items-center justify-center gap-2 rounded-lg py-4 font-bold transition-all active:scale-[0.98] ${
              canSubmit
                ? "cursor-pointer bg-primary text-background hover:opacity-90"
                : "cursor-not-allowed bg-surface-container-high text-[#555555]"
            }`}
          >
            {busy ? "Analyzing…" : "Analyze requirements"}
            {!busy && (
              <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
            )}
          </button>

          {(localError || error) && (
            <p className="text-label-md text-center text-error">{localError || error}</p>
          )}
        </div>

        <div className="mt-8 flex items-center gap-2 opacity-40">
          <div className="h-2 w-2 rounded-full bg-outline" />
          <p className="text-label-md uppercase tracking-widest text-on-surface-variant">
            Untrusted input · treated as data only
          </p>
        </div>
      </div>
    </main>
  );
}
