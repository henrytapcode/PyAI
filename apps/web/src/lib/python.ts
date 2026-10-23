"use client";

import { useSyncExternalStore } from "react";
import type { TestRunResult, TraceResult } from "./types";

export type PyStatus = "idle" | "loading" | "ready" | "running" | "error";

type Pending = {
  resolve: (value: unknown) => void;
  onOutput?: (text: string, stream: "stdout" | "stderr") => void;
  timer?: ReturnType<typeof setTimeout>;
  kind: "run" | "test" | "trace";
};

export interface RunResult {
  ok: boolean;
  error: string | null;
  stopped?: boolean;
  timedOut?: boolean;
}

const TEST_TIMEOUT_MS = 15_000;
const RUN_TIMEOUT_MS = 60_000;

class PythonManager {
  private worker: Worker | null = null;
  private pending = new Map<number, Pending>();
  private nextId = 1;
  private listeners = new Set<() => void>();
  status: PyStatus = "idle";
  version: string | null = null;
  lastError: string | null = null;

  subscribe = (fn: () => void) => {
    this.listeners.add(fn);
    return () => this.listeners.delete(fn);
  };

  private setStatus(status: PyStatus) {
    this.status = status;
    this.listeners.forEach((fn) => fn());
  }

  /** Start loading Pyodide in the background (safe to call many times). */
  warmUp() {
    this.ensureWorker();
  }

  private ensureWorker(): Worker {
    if (this.worker) return this.worker;
    const worker = new Worker(`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/pyodide-worker.js`);
    worker.onmessage = (e: MessageEvent) => this.onMessage(e.data);
    worker.onerror = (e) => {
      this.lastError = e.message || "worker error";
      this.setStatus("error");
    };
    this.worker = worker;
    this.setStatus("loading");
    worker.postMessage({ type: "init" });
    return worker;
  }

  private onMessage(msg: { type: string; id?: number; [k: string]: unknown }) {
    const p = msg.id != null ? this.pending.get(msg.id) : undefined;
    switch (msg.type) {
      case "status":
        if (this.pending.size === 0) this.setStatus(msg.status as PyStatus);
        break;
      case "ready":
        this.version = String(msg.version);
        if (this.pending.size === 0) this.setStatus("ready");
        break;
      case "fatal":
        this.lastError = String(msg.error);
        this.setStatus("error");
        this.pending.forEach((pp) => pp.resolve({ ok: false, error: this.lastError }));
        this.pending.clear();
        break;
      case "stdout":
      case "stderr":
        p?.onOutput?.(String(msg.text), msg.type);
        break;
      case "done":
        if (p && msg.id != null) this.finish(msg.id, { ok: Boolean(msg.ok), error: (msg.error as string) ?? null });
        break;
      case "result":
        if (p && msg.id != null) this.finish(msg.id, msg.result);
        break;
    }
  }

  private finish(id: number, value: unknown) {
    const p = this.pending.get(id);
    if (!p) return;
    if (p.timer) clearTimeout(p.timer);
    this.pending.delete(id);
    p.resolve(value);
    if (this.pending.size === 0) this.setStatus("ready");
  }

  private send<T>(kind: Pending["kind"], payload: object, timeoutMs: number, onOutput?: Pending["onOutput"]): Promise<T> {
    const worker = this.ensureWorker();
    const id = this.nextId++;
    return new Promise<T>((resolve) => {
      const entry: Pending = { resolve: resolve as (v: unknown) => void, onOutput, kind };
      entry.timer = setTimeout(() => this.restart({ timedOut: true }), timeoutMs);
      this.pending.set(id, entry);
      this.setStatus("running");
      worker.postMessage({ ...payload, id });
    });
  }

  run(code: string, onOutput?: Pending["onOutput"]): Promise<RunResult> {
    return this.send<RunResult>("run", { type: "run", code }, RUN_TIMEOUT_MS, onOutput);
  }

  test(code: string, tests: string): Promise<TestRunResult> {
    return this.send<TestRunResult>("test", { type: "test", code, tests }, TEST_TIMEOUT_MS);
  }

  /** Step-by-step execution trace for the Visualize view. */
  trace(code: string): Promise<TraceResult> {
    return this.send<TraceResult>("trace", { type: "trace", code }, TEST_TIMEOUT_MS);
  }

  /** Kill the worker (stops infinite loops), resolve pending calls, start a fresh one. */
  restart(reason: { timedOut?: boolean; stopped?: boolean } = { stopped: true }) {
    const pending = [...this.pending.values()];
    this.pending.clear();
    this.worker?.terminate();
    this.worker = null;
    for (const p of pending) {
      if (p.timer) clearTimeout(p.timer);
      if (p.kind === "test") {
        p.resolve({ ok: false, passed: 0, total: 0, tests: [], error: null, stdout: "", timedOut: true } satisfies TestRunResult);
      } else if (p.kind === "trace") {
        p.resolve({ steps: [], stdout: "", error: null, truncated: false, timedOut: true } satisfies TraceResult);
      } else {
        p.resolve({ ok: false, error: null, ...reason } satisfies RunResult);
      }
    }
    this.setStatus("idle");
    this.ensureWorker();
  }
}

export const python = typeof window !== "undefined" ? new PythonManager() : (null as unknown as PythonManager);

export function usePythonStatus(): PyStatus {
  return useSyncExternalStore(
    (fn) => (python ? python.subscribe(fn) : () => {}),
    () => (python ? python.status : "idle"),
    () => "idle",
  );
}
