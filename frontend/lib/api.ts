// Typed fetch helpers. No secrets here — all model calls happen server-side.
// Mirrors spec/backend_specs/CONTRACT.md exactly.

export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

export interface Suggestion {
  strategy_id: string;
  title: string;
  rationale: string;
  target_signal: string;
  on_brand: boolean;
}

export interface SpecFileMeta {
  name: string;
  mime: string;
}

export interface SpecFileFull extends SpecFileMeta {
  content: string;
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function jsonOrThrow<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body?.detail ?? detail;
    } catch {
      /* non-JSON error body */
    }
    throw new ApiError(res.status, String(detail));
  }
  return res.json() as Promise<T>;
}

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return jsonOrThrow<T>(res);
}

// POST /upload — multipart .txt/.md only. Returns the document id.
export async function uploadFile(file: File): Promise<{ document_id: string }> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: form });
  return jsonOrThrow(res);
}

// Pasted text -> wrap as a .md file for the same /upload endpoint.
export function uploadText(text: string): Promise<{ document_id: string }> {
  const file = new File([text], "brief.md", { type: "text/markdown" });
  return uploadFile(file);
}

export function analyze(documentId: string): Promise<{ analysis_id: string }> {
  return postJson("/analyze", { document_id: documentId });
}

export function refine(
  analysisId: string,
  feedback: string,
): Promise<{ analysis_id: string; iteration: number }> {
  return postJson("/refine", { analysis_id: analysisId, feedback });
}

export async function sendFeedback(
  strategyId: string,
  action: "approve" | "reject",
): Promise<void> {
  const res = await fetch(`${API_BASE}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ strategy_id: strategyId, action }),
  });
  if (!res.ok && res.status !== 204) {
    throw new ApiError(res.status, "feedback failed");
  }
}

export function generateSpecs(
  analysisId: string,
  approvedIds: string[],
): Promise<{ spec_id: string; files: SpecFileFull[] }> {
  return postJson("/generate-specs", {
    analysis_id: analysisId,
    approved_ids: approvedIds,
  });
}

// GET /specs/{id}/{name} — download (attachment, sanitized filename).
export function specFileUrl(specId: string, name: string): string {
  return `${API_BASE}/specs/${specId}/${encodeURIComponent(name)}`;
}
