// Typed fetch helpers. No secrets here — all model calls happen server-side.

export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

export interface Question {
  id: string;
  question: string;
  why: string;
  suggestions: string[];
}

export interface SpecFileMeta {
  path: string;
  mime: string;
}

export interface Answer {
  id: string;
  answer: string;
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
      detail = (await res.json())?.detail ?? detail;
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

// POST /upload — multipart .txt/.md only.
export async function uploadFile(file: File): Promise<{ document_id: string }> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: form });
  return jsonOrThrow(res);
}

// Pasted brief -> wrap as a .md file for the same /upload endpoint.
export function uploadText(text: string): Promise<{ document_id: string }> {
  const file = new File([text], "brief.md", { type: "text/markdown" });
  return uploadFile(file);
}

export function analyze(documentId: string): Promise<{ analysis_id: string }> {
  return postJson("/analyze", { document_id: documentId });
}

export function generateSpecs(
  analysisId: string,
  answers: Answer[],
): Promise<{ spec_id: string }> {
  return postJson("/generate-specs", { analysis_id: analysisId, answers });
}

export function refine(
  analysisId: string,
  feedback: string,
): Promise<{ spec_id: string }> {
  return postJson("/refine", { analysis_id: analysisId, feedback });
}

export function zipUrl(specId: string): string {
  return `${API_BASE}/specs/${specId}/archive.zip`;
}

export function fileUrl(specId: string, path: string): string {
  const encoded = path.split("/").map(encodeURIComponent).join("/");
  return `${API_BASE}/specs/${specId}/file/${encoded}`;
}
