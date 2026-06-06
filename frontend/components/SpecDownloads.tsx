"use client";

import { specFileUrl, type SpecFileMeta } from "@/lib/api";

function triggerDownload(url: string) {
  const a = document.createElement("a");
  a.href = url;
  a.rel = "noopener";
  // Server sets Content-Disposition: attachment, so this forces a download
  // even cross-origin.
  document.body.appendChild(a);
  a.click();
  a.remove();
}

const ICON: Record<string, string> = {
  "text/markdown": "description",
  "application/json": "data_object",
};

export function SpecDownloads({
  specId,
  files,
}: {
  specId: string;
  files: SpecFileMeta[];
}) {
  function downloadAll() {
    files.forEach((f, i) =>
      setTimeout(() => triggerDownload(specFileUrl(specId, f.name)), i * 250),
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-4 pt-12">
      <div className="flex w-full max-w-[460px] flex-col items-center">
        <div className="mb-8 flex flex-col items-center text-center">
          <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-xl border border-outline bg-surface-container-high">
            <span className="material-symbols-outlined text-[32px] text-primary">
              task_alt
            </span>
          </div>
          <h1 className="text-headline-lg mb-1 text-primary">Your specs are ready</h1>
          <p className="text-body-lg text-on-surface-variant">
            {files.length} file{files.length === 1 ? "" : "s"} generated from your approved
            strategies.
          </p>
        </div>

        {/* Primary download-all card */}
        <button
          onClick={downloadAll}
          className="group flex h-[120px] w-full max-w-[400px] flex-col items-center justify-center gap-2 rounded-[10px] border border-transparent bg-[#f2f2f2] text-[#1a1a1a] transition-all hover:border-primary/20 active:scale-[0.98]"
        >
          <span className="material-symbols-outlined text-[40px] transition-transform duration-300 group-hover:-translate-y-1">
            download
          </span>
          <span className="text-body-lg font-bold">Download all files</span>
        </button>

        <div className="mt-4 flex items-center gap-1 text-secondary">
          <span
            className="material-symbols-outlined text-[16px]"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            check_circle
          </span>
          <span className="text-label-md">Verified · guardrails applied</span>
        </div>

        {/* Individual files */}
        <div className="mt-8 flex w-full flex-col gap-2">
          {files.map((f) => (
            <a
              key={f.name}
              href={specFileUrl(specId, f.name)}
              className="flex items-center justify-between rounded-lg border border-outline-variant bg-surface-container-low px-4 py-3 transition-colors hover:border-outline"
            >
              <span className="flex items-center gap-2">
                <span className="material-symbols-outlined text-[20px] text-on-surface-variant">
                  {ICON[f.mime] ?? "draft"}
                </span>
                <span className="text-code-md text-primary">{f.name}</span>
              </span>
              <span className="material-symbols-outlined text-[18px] text-on-surface-variant">
                download
              </span>
            </a>
          ))}
        </div>
      </div>
    </main>
  );
}
