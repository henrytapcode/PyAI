"use client";

import { createContext, useContext, useSyncExternalStore } from "react";
import type { RunResult, RunnerKind } from "./python";
import type { TestRunResult, TraceResult } from "./types";

export type LocalRunnerStatus = "unknown" | "checking" | "connected" | "offline" | "running";

export interface LocalRunnerInfo {
  python: string | null;
  torch: string | null;
  transformers?: string | null;
}

export type LocalTestRunResult = TestRunResult & { offline?: boolean; stopped?: boolean };
export type LocalTraceResult = TraceResult & { offline?: boolean; stopped?: boolean };

const BASE_URL = (process.env.NEXT_PUBLIC_LOCAL_RUNNER_URL || "http://127.0.0.1:8765").replace(/\/+$/, "");

const HEALTH_TIMEOUT_MS = 3_000;
const RUN_TIMEOUT_MS = 130_000;
const TEST_TIMEOUT_MS = 70_000;
const TRACE_TIMEOUT_MS = 40_000;
export const OUTPUT_FLUSH_MS = 150;

type TextStream = "stdout" | "stderr";

function createStreamBuffer(onOutput?: (text: string, stream: "stdout" | "stderr" | "image") => void) {
  const buffers: Record<TextStream, string> = { stdout: "", stderr: "" };
  const timers: Record<TextStream, ReturnType<typeof setTimeout> | null> = { stdout: null, stderr: null };
  const pendingOrder: TextStream[] = [];

  const clearTimer = (stream: TextStream) => {
    const timer = timers[stream];
    if (timer !== null) {
      clearTimeout(timer);
      timers[stream] = null;
    }
  };

  const removePending = (stream: TextStream) => {
    const idx = pendingOrder.indexOf(stream);
    if (idx !== -1) pendingOrder.splice(idx, 1);
  };

  const flushStream = (stream: TextStream) => {
    clearTimer(stream);
    removePending(stream);
    const rest = buffers[stream];
    if (rest) {
      buffers[stream] = "";
      onOutput?.(rest, stream);
    }
  };

  const push = (stream: TextStream, text: string) => {
    if (!text) return;
    clearTimer(stream);
    buffers[stream] += text;
    let nl = buffers[stream].indexOf("\n");
    while (nl !== -1) {
      const line = buffers[stream].slice(0, nl);
      buffers[stream] = buffers[stream].slice(nl + 1);
      onOutput?.(`${line}\n`, stream);
      nl = buffers[stream].indexOf("\n");
    }
    if (buffers[stream].length > 0) {
      if (!pendingOrder.includes(stream)) {
        pendingOrder.push(stream);
      }
      timers[stream] = setTimeout(() => flushStream(stream), OUTPUT_FLUSH_MS);
    } else {
      removePending(stream);
    }
  };

  const flushAll = () => {
    for (const stream of [...pendingOrder]) {
      flushStream(stream);
    }
    flushStream("stdout");
    flushStream("stderr");
  };

  const dispose = () => {
    clearTimer("stdout");
    clearTimer("stderr");
  };

  return { push, flushAll, dispose };
}

const POST_HEADERS = {
  "Content-Type": "application/json",
  "X-PyAI-Runner": "1",
} as const;

type ActiveRequest = {
  controller: AbortController;
  reason: "stop" | "timeout" | null;
};

async function readErrorDetail(res: Response): Promise<string> {
  try {
    const data = (await res.json()) as { detail?: unknown };
    if (typeof data?.detail === "string" && data.detail) return data.detail;
  } catch {
    /* non-json error response */
  }
  return `HTTP ${res.status}`;
}

export class LocalRunner {
  private listeners = new Set<() => void>();
  private queue: Promise<void> = Promise.resolve();
  private inFlight = 0;
  private active: ActiveRequest | null = null;
  private checkPromise: Promise<boolean> | null = null;

  status: LocalRunnerStatus = "unknown";
  info: LocalRunnerInfo | null = null;

  subscribe = (fn: () => void) => {
    this.listeners.add(fn);
    return () => this.listeners.delete(fn);
  };

  private setStatus(status: LocalRunnerStatus) {
    this.status = status;
    this.listeners.forEach((fn) => fn());
  }

  /** Probe `/health` with a 3s timeout; preserves `running` status if a job is active. */
  check(): Promise<boolean> {
    if (this.checkPromise) return this.checkPromise;
    const promise = (async () => {
      if (this.status !== "running") {
        this.setStatus("checking");
      }
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), HEALTH_TIMEOUT_MS);
      try {
        const res = await fetch(`${BASE_URL}/health`, {
          method: "GET",
          signal: controller.signal,
          cache: "no-store",
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = (await res.json()) as {
          protocol?: unknown;
          python?: unknown;
          torch?: unknown;
          transformers?: unknown;
        };
        if (data?.protocol !== 1) throw new Error("Unsupported protocol");
        this.info = {
          python: typeof data.python === "string" ? data.python : null,
          torch: typeof data.torch === "string" ? data.torch : null,
          transformers: typeof data.transformers === "string" ? data.transformers : null,
        };
        if (this.status !== "running") {
          this.setStatus("connected");
        }
        return true;
      } catch {
        if (this.status !== "running") {
          this.info = null;
          this.setStatus("offline");
        }
        return false;
      } finally {
        clearTimeout(timer);
        this.checkPromise = null;
      }
    })();
    this.checkPromise = promise;
    return promise;
  }

  private enqueue<T>(fn: () => Promise<T>): Promise<T> {
    this.inFlight += 1;
    const next = this.queue.then(fn, fn);
    this.queue = next.then(
      () => undefined,
      () => undefined,
    );
    return next.finally(() => {
      this.inFlight -= 1;
    });
  }

  private beginRequest(timeoutMs: number): { active: ActiveRequest; clear: () => void } {
    this.setStatus("running");
    const active: ActiveRequest = { controller: new AbortController(), reason: null };
    this.active = active;
    const timer = setTimeout(() => {
      active.reason = "timeout";
      active.controller.abort();
    }, timeoutMs);
    return {
      active,
      clear: () => {
        clearTimeout(timer);
        if (this.active === active) {
          this.active = null;
        }
      },
    };
  }

  private finishConnected() {
    if (this.inFlight <= 1 && this.status === "running") {
      this.setStatus("connected");
    }
  }

  private markOffline() {
    this.info = null;
    this.setStatus("offline");
  }

  run(code: string, onOutput?: (text: string, stream: "stdout" | "stderr" | "image") => void): Promise<RunResult> {
    return this.enqueue(async (): Promise<RunResult> => {
      const { active, clear } = this.beginRequest(RUN_TIMEOUT_MS);
      const streamBuffer = createStreamBuffer(onOutput);
      let reader: ReadableStreamDefaultReader<Uint8Array> | null = null;
      try {
        const res = await fetch(`${BASE_URL}/run`, {
          method: "POST",
          headers: POST_HEADERS,
          body: JSON.stringify({ code }),
          signal: active.controller.signal,
        });
        if (!res.ok) {
          const detail = await readErrorDetail(res);
          this.finishConnected();
          return { ok: false, error: detail };
        }
        if (!res.body) {
          this.finishConnected();
          return { ok: false, error: "Empty response stream" };
        }

        reader = res.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let buffer = "";
        let doneResult: RunResult | null = null;

        const processLine = (line: string) => {
          const trimmed = line.trim();
          if (!trimmed) return;
          let msg: Record<string, unknown>;
          try {
            msg = JSON.parse(trimmed) as Record<string, unknown>;
          } catch {
            return;
          }
          const kind = msg.type;
          if (kind === "stdout" || kind === "stderr") {
            streamBuffer.push(kind, String(msg.text ?? ""));
          } else if (kind === "image") {
            streamBuffer.flushAll();
            onOutput?.(String(msg.data ?? ""), "image");
          } else if (kind === "done") {
            streamBuffer.flushAll();
            doneResult = {
              ok: Boolean(msg.ok),
              error: typeof msg.error === "string" ? msg.error : null,
              ...(msg.timedOut ? { timedOut: true } : {}),
            };
          }
        };

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          let nl = buffer.indexOf("\n");
          while (nl !== -1) {
            processLine(buffer.slice(0, nl));
            buffer = buffer.slice(nl + 1);
            nl = buffer.indexOf("\n");
          }
        }
        buffer += decoder.decode();
        if (buffer.trim()) {
          processLine(buffer);
        }
        streamBuffer.flushAll();

        this.finishConnected();
        return doneResult ?? { ok: false, error: "Runner stream ended unexpectedly" };
      } catch {
        streamBuffer.flushAll();
        if (active.reason === "stop") {
          this.finishConnected();
          return { ok: false, error: null, stopped: true };
        }
        if (active.reason === "timeout") {
          this.finishConnected();
          return { ok: false, error: null, timedOut: true };
        }
        this.markOffline();
        return { ok: false, error: null, offline: true };
      } finally {
        streamBuffer.dispose();
        clear();
        if (reader) {
          reader.cancel().catch(() => {});
        }
      }
    });
  }

  test(code: string, tests: string): Promise<LocalTestRunResult> {
    return this.enqueue(async (): Promise<LocalTestRunResult> => {
      const { active, clear } = this.beginRequest(TEST_TIMEOUT_MS);
      try {
        const res = await fetch(`${BASE_URL}/test`, {
          method: "POST",
          headers: POST_HEADERS,
          body: JSON.stringify({ code, tests }),
          signal: active.controller.signal,
        });
        if (!res.ok) {
          const detail = await readErrorDetail(res);
          this.finishConnected();
          return {
            ok: false,
            passed: 0,
            total: 0,
            tests: [],
            error: { type: "RunnerError", message: detail, line: null },
            stdout: "",
          };
        }
        const data = (await res.json()) as LocalTestRunResult;
        this.finishConnected();
        return data;
      } catch {
        if (active.reason === "stop") {
          this.finishConnected();
          return { ok: false, passed: 0, total: 0, tests: [], error: null, stdout: "", stopped: true };
        }
        if (active.reason === "timeout") {
          this.finishConnected();
          return { ok: false, passed: 0, total: 0, tests: [], error: null, stdout: "", timedOut: true };
        }
        this.markOffline();
        return { ok: false, passed: 0, total: 0, tests: [], error: null, stdout: "", offline: true };
      } finally {
        clear();
      }
    });
  }

  trace(code: string): Promise<LocalTraceResult> {
    return this.enqueue(async (): Promise<LocalTraceResult> => {
      const { active, clear } = this.beginRequest(TRACE_TIMEOUT_MS);
      try {
        const res = await fetch(`${BASE_URL}/trace`, {
          method: "POST",
          headers: POST_HEADERS,
          body: JSON.stringify({ code }),
          signal: active.controller.signal,
        });
        if (!res.ok) {
          const detail = await readErrorDetail(res);
          this.finishConnected();
          return {
            steps: [],
            stdout: "",
            error: { type: "RunnerError", message: detail, line: null },
            truncated: false,
          };
        }
        const data = (await res.json()) as LocalTraceResult;
        this.finishConnected();
        return data;
      } catch {
        if (active.reason === "stop") {
          this.finishConnected();
          return { steps: [], stdout: "", error: null, truncated: false, stopped: true };
        }
        if (active.reason === "timeout") {
          this.finishConnected();
          return { steps: [], stdout: "", error: null, truncated: false, timedOut: true };
        }
        this.markOffline();
        return { steps: [], stdout: "", error: null, truncated: false, offline: true };
      } finally {
        clear();
      }
    });
  }

  /** Abort the currently active request (the server kills the child subprocess). */
  stop() {
    if (this.active) {
      this.active.reason = "stop";
      this.active.controller.abort();
    }
  }
}

export const localRunner = typeof window !== "undefined" ? new LocalRunner() : (null as unknown as LocalRunner);

export function useLocalRunnerStatus(): LocalRunnerStatus {
  return useSyncExternalStore(
    (fn) => (localRunner ? localRunner.subscribe(fn) : () => {}),
    () => (localRunner ? localRunner.status : "unknown"),
    () => "unknown",
  );
}

export const RunnerContext = createContext<RunnerKind | undefined>(undefined);

export function useRunner(): RunnerKind | undefined {
  return useContext(RunnerContext);
}
