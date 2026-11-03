import { createClient, type SupabaseClient } from "@supabase/supabase-js";

export function getRagUrl(): string {
  return (process.env.NEXT_PUBLIC_RAG_URL || "").trim().replace(/\/+$/, "");
}

export const isRagConfigured = Boolean(process.env.NEXT_PUBLIC_RAG_URL);

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const isAuthEnabled = Boolean(SUPABASE_URL && SUPABASE_ANON_KEY);

export interface SourceItem {
  n: number;
  title: string;
  heading: string;
  lesson_id: string | null;
  url: string | null;
  path: string;
  kind: string | null;
}

export interface AskPayload {
  question: string;
  exercise?: string | null;
  provider?: "claude" | "gemini" | null;
}

export interface HintNextPayload {
  question: string;
  exercise?: string | null;
  provider?: "claude" | "gemini" | null;
  current_tier?: number | null;
}

export interface RagResponse {
  answer: string;
  refused: boolean;
  lang: string;
  cited: number[];
  sources: SourceItem[];
  tier: number | null;
}

export interface HealthResponse {
  status: string;
  index_chunks: number;
}

export class RagApiError extends Error {
  status: number;
  retryAfter: number | null;

  constructor(
    status: number,
    message: string,
    retryAfter?: number | null,
  ) {
    super(message);
    this.name = "RagApiError";
    this.status = status;
    this.retryAfter = retryAfter ?? null;
  }
}

let ragAuthClient: SupabaseClient | null = null;

/**
 * Retrieves the active Supabase session access token if available.
 * Never logs or persists the token elsewhere.
 */
async function getSupabaseToken(): Promise<string | null> {
  if (typeof window === "undefined" || !isAuthEnabled) return null;
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  if (!url || !key) return null;
  try {
    if (!ragAuthClient) {
      ragAuthClient = createClient(url, key, {
        auth: { persistSession: true, autoRefreshToken: false, detectSessionInUrl: false },
      });
    }
    const { data } = await ragAuthClient.auth.getSession();
    return data.session?.access_token ?? null;
  } catch {
    return null;
  }
}

/**
 * Common helper to POST to RAG API with timeout, abort handling, and auth headers.
 */
async function postRag<T>(
  endpoint: string,
  payload: Record<string, unknown>,
  signal?: AbortSignal,
  timeoutMs: number = 60000,
): Promise<T> {
  const baseUrl = getRagUrl();
  if (!baseUrl) {
    throw new RagApiError(0, "RAG backend URL is not configured");
  }

  // Safety invariant: never transmit answers flag or solution requests
  const safePayload: Record<string, unknown> = { ...payload };
  delete safePayload.answers;
  delete safePayload.allow_solution;

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  if (signal) {
    if (signal.aborted) {
      controller.abort();
    } else {
      signal.addEventListener("abort", () => controller.abort(), { once: true });
    }
  }

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Accept: "application/json",
  };

  try {
    const token = await getSupabaseToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const res = await fetch(`${baseUrl}${endpoint}`, {
      method: "POST",
      headers,
      body: JSON.stringify(safePayload),
      signal: controller.signal,
    });

    if (!res.ok) {
      let retryAfter: number | null = null;
      if (res.status === 429) {
        const retryHeader = res.headers.get("Retry-After");
        if (retryHeader) {
          const parsed = parseInt(retryHeader, 10);
          if (!isNaN(parsed) && parsed > 0) {
            retryAfter = parsed;
          }
        }
      }

      let detailMsg = `HTTP ${res.status}`;
      try {
        const body = await res.json();
        if (body && typeof body.detail === "string") {
          detailMsg = body.detail;
        }
      } catch {
        // Fall back to HTTP status message
      }

      throw new RagApiError(res.status, detailMsg, retryAfter);
    }

    return (await res.json()) as T;
  } catch (err: unknown) {
    if (err instanceof RagApiError) throw err;
    if (err instanceof DOMException && err.name === "AbortError") {
      throw new RagApiError(503, "Request timed out or was cancelled");
    }
    throw new RagApiError(503, "Network error or service unavailable");
  } finally {
    clearTimeout(timeoutId);
  }
}

/**
 * Checks health of the RAG backend service.
 */
export async function checkHealth(signal?: AbortSignal): Promise<HealthResponse> {
  const baseUrl = getRagUrl();
  if (!baseUrl) {
    throw new RagApiError(0, "RAG backend URL is not configured");
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000);

  if (signal) {
    if (signal.aborted) {
      controller.abort();
    } else {
      signal.addEventListener("abort", () => controller.abort(), { once: true });
    }
  }

  try {
    const res = await fetch(`${baseUrl}/health`, {
      method: "GET",
      headers: { Accept: "application/json" },
      signal: controller.signal,
    });
    if (!res.ok) {
      throw new RagApiError(res.status, `Health check returned HTTP ${res.status}`);
    }
    return (await res.json()) as HealthResponse;
  } catch (err: unknown) {
    if (err instanceof RagApiError) throw err;
    if (err instanceof DOMException && err.name === "AbortError") {
      throw new RagApiError(503, "Health check timed out");
    }
    throw new RagApiError(503, "Failed to reach RAG backend");
  } finally {
    clearTimeout(timeoutId);
  }
}

/**
 * Sends a learning question to the RAG backend.
 */
export async function askRag(payload: AskPayload, signal?: AbortSignal): Promise<RagResponse> {
  return postRag<RagResponse>("/ask", payload as unknown as Record<string, unknown>, signal);
}

/**
 * Requests the next progressive hint tier for an exercise.
 */
export async function nextHint(payload: HintNextPayload, signal?: AbortSignal): Promise<RagResponse> {
  return postRag<RagResponse>("/hint-next", payload as unknown as Record<string, unknown>, signal);
}

