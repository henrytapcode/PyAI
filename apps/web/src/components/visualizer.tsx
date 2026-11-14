"use client";

import { ArrowRight, ChevronFirst, ChevronLast, ChevronLeft, ChevronRight, Eye, Loader2, Pause, Play } from "lucide-react";
import { useTranslations } from "next-intl";
import { Fragment, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { LocalRunnerSetup } from "@/components/local-runner-setup";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog";
import type { LocalTraceResult } from "@/lib/local-runner";
import { runnerFor, type RunnerKind } from "@/lib/python";
import type { TraceStep } from "@/lib/types";
import { cn } from "@/lib/utils";

type VisualizerState = { code: string; runner?: RunnerKind } | null;

let openVisualizer: ((code: string, runner?: RunnerKind) => void) | null = null;

/** Open the step-through view for a piece of code from anywhere (a lesson block, the editor...). */
export function visualize(code: string, runner?: RunnerKind) {
  openVisualizer?.(code, runner);
}

/** Mounted once (in the app shell). Renders the dialog when `visualize()` is called. */
export function VisualizerHost() {
  const [state, setState] = useState<VisualizerState>(null);
  useEffect(() => {
    openVisualizer = (code, runner) => setState({ code, runner });
    return () => {
      openVisualizer = null;
    };
  }, []);
  return (
    <Dialog open={!!state} onOpenChange={(o) => !o && setState(null)}>
      <DialogContent className="flex h-[min(88dvh,760px)] max-w-6xl flex-col gap-3 overflow-hidden p-0 sm:p-0">
        {state && <Visualizer key={`${state.runner ?? "pyodide"}:${state.code}`} code={state.code} runner={state.runner} />}
      </DialogContent>
    </Dialog>
  );
}

function Visualizer({ code, runner }: { code: string; runner?: RunnerKind }) {
  const t = useTranslations("visualize");
  const [result, setResult] = useState<LocalTraceResult | null>(null);
  const [retryTick, setRetryTick] = useState(0);
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    let alive = true;
    setResult(null);
    runnerFor(runner)
      .trace(code)
      .then((r) => {
        if (alive) setResult(r);
      });
    return () => {
      alive = false;
    };
  }, [code, runner, retryTick]);

  const steps = result?.steps ?? [];
  const last = Math.max(0, steps.length - 1);
  const step = steps[index] as TraceStep | undefined;
  const prev = index > 0 ? steps[index - 1] : undefined;
  const go = useCallback((i: number) => setIndex(Math.max(0, Math.min(last, i))), [last]);

  // Autoplay
  useEffect(() => {
    if (!playing) return;
    if (index >= last) {
      setPlaying(false);
      return;
    }
    const id = setTimeout(() => setIndex((i) => i + 1), 650);
    return () => clearTimeout(id);
  }, [playing, index, last]);

  // Keyboard: ← → Home End, space to play
  useEffect(() => {
    if (steps.length === 0) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight") go(index + 1);
      else if (e.key === "ArrowLeft") go(index - 1);
      else if (e.key === "Home") go(0);
      else if (e.key === "End") go(last);
      else if (e.key === " ") {
        e.preventDefault();
        setPlaying((p) => !p);
      } else return;
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [go, index, last, steps.length]);

  const lines = useMemo(() => code.replace(/\n$/, "").split("\n"), [code]);
  const atEnd = index === last;
  const output = result ? (atEnd ? result.stdout : result.stdout.slice(0, step?.out ?? 0)) : "";
  const lineRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    lineRef.current?.scrollIntoView({ block: "nearest" });
  }, [index]);

  const caption = !step
    ? ""
    : step.event === "return"
      ? t("returns", { name: step.stack[step.stack.length - 1]?.name ?? "", value: step.ret ?? "None" })
      : step.event === "exception"
        ? t("raised", { error: step.ret ?? "" })
        : t("aboutToRun", { line: step.line });

  return (
    <>
      <div className="flex flex-wrap items-center gap-3 border-b px-5 py-3 pr-12">
        <Eye className="size-5 text-primary" aria-hidden="true" />
        <div className="min-w-0 flex-1">
          <DialogTitle className="text-base">{t("title")}</DialogTitle>
          <DialogDescription className="text-xs">{t("subtitle")}</DialogDescription>
        </div>
        {result && steps.length > 0 && (
          <span className="text-xs tabular-nums text-muted-foreground">{t("step", { n: index + 1, total: steps.length })}</span>
        )}
      </div>

      {!result ? (
        <div className="grid flex-1 place-items-center text-sm text-muted-foreground">
          <span className="flex items-center gap-2">
            <Loader2 className="size-4 animate-spin text-primary" aria-hidden="true" /> {t("tracing")}
          </span>
        </div>
      ) : result.offline ? (
        <div className="min-h-0 flex-1 overflow-auto p-5">
          <LocalRunnerSetup onConnected={() => setRetryTick((n) => n + 1)} />
        </div>
      ) : result.timedOut ? (
        <p className="m-5 rounded-md border border-danger/20 bg-danger-soft p-3 text-sm text-danger">{t("timedOut")}</p>
      ) : steps.length === 0 ? (
        <div className="m-5 space-y-2">
          {result.error ? (
            <pre className="whitespace-pre-wrap rounded-md border border-danger/20 bg-danger-soft p-3 font-mono text-xs text-danger">
              {result.error.type}: {result.error.message}
              {result.error.line ? ` (${t("line", { line: result.error.line })})` : ""}
            </pre>
          ) : (
            <p className="text-sm text-muted-foreground">{t("nothing")}</p>
          )}
        </div>
      ) : (
        <div className="grid min-h-0 flex-1 gap-0 md:grid-cols-[minmax(0,1.1fr)_minmax(0,1fr)]">
          {/* Code with the current line */}
          <div className="min-h-0 overflow-auto border-b bg-code py-3 font-mono text-xs leading-6 md:border-b-0 md:border-r">
            {lines.map((text, i) => {
              const n = i + 1;
              const current = step?.line === n;
              const previous = !current && prev?.line === n;
              return (
                <div
                  key={n}
                  ref={current ? lineRef : undefined}
                  className={cn(
                    "flex gap-3 px-3 border-l-[3px] border-transparent transition-colors",
                    current && (step?.event === "exception" ? "bg-danger-soft border-l-danger text-danger" : "bg-accent border-l-primary text-primary font-medium"),
                    previous && "bg-muted/40",
                  )}
                >
                  <span className="flex items-center justify-end w-5 shrink-0 select-none font-mono text-xs text-muted-foreground/70">{current ? <ArrowRight className="size-3.5 text-primary" aria-hidden="true" /> : n}</span>
                  <span className="whitespace-pre">{text || " "}</span>
                </div>
              );
            })}
          </div>

          {/* State */}
          <div className="flex min-h-0 flex-col overflow-auto p-4">
            <p className={cn("mb-3 rounded-md border px-3 py-2 text-sm", step?.event === "exception" ? "border-danger/20 bg-danger-soft text-danger" : "border-border bg-accent/60 text-foreground")}>{caption}</p>
            <div className="space-y-3">
              {step?.stack.map((frame, fi) => {
                const before = prev?.stack[fi]?.name === frame.name ? prev.stack[fi] : undefined;
                return (
                  <div key={`${fi}-${frame.name}`} className={cn("rounded-lg border border-border bg-card overflow-hidden", fi === step.stack.length - 1 && "border-primary")}>
                    <div className="flex items-center gap-2 border-b border-border bg-muted/40 px-3 py-1.5 text-xs font-bold text-foreground">
                      {frame.name === "global" ? t("globals") : t("frame", { name: frame.name })}
                    </div>
                    {frame.vars.length === 0 ? (
                      <p className="px-3 py-2 text-xs text-muted-foreground">{t("noVars")}</p>
                    ) : (
                      <table className="w-full text-xs font-mono">
                        <tbody>
                          {frame.vars.map((v) => {
                            const old = before?.vars.find((x) => x.name === v.name);
                            const changed = !old || old.repr !== v.repr || JSON.stringify(old.table) !== JSON.stringify(v.table);
                            const isChanged = changed && index > 0;
                            const table = v.table;
                            const isPartial = table ? table.shape[0] > table.rows.length || table.shape[1] > table.columns.length : false;
                            return (
                              <Fragment key={v.name}>
                                <tr className={cn(!table && "border-b border-border/50 last:border-0", isChanged && "bg-warning-soft text-warning-ink transition-colors")}>
                                  <td className="w-1/3 px-3 py-1.5 font-medium">{v.name}</td>
                                  <td className="px-3 py-1.5 break-all">
                                    {table ? (
                                      <span className="text-muted-foreground">{t("tableShape", { rows: table.shape[0], cols: table.shape[1] })}</span>
                                    ) : (
                                      v.repr
                                    )}
                                  </td>
                                  <td className="w-0 px-3 py-1.5 text-right">
                                    <Badge variant="muted" className="font-mono">
                                      {v.type}
                                    </Badge>
                                  </td>
                                </tr>
                                {table && (
                                  <tr className={cn("border-b border-border/50 last:border-0", isChanged && "bg-warning-soft text-warning-ink transition-colors")}>
                                    <td colSpan={3} className="px-3 pb-2.5 pt-0.5">
                                      <div className="w-0 min-w-full overflow-x-auto">
                                        <table className="border-collapse border border-border bg-card font-mono text-[11px] text-foreground">
                                          <thead>
                                            <tr className="bg-muted/40">
                                              <th className="border border-border px-2 py-1 whitespace-nowrap" />
                                              {table.columns.map((col, ci) => (
                                                <th key={ci} className="border border-border px-2 py-1 text-left font-medium whitespace-nowrap">
                                                  {col}
                                                </th>
                                              ))}
                                            </tr>
                                          </thead>
                                          <tbody>
                                            {table.rows.map((row, ri) => (
                                              <tr key={ri}>
                                                <th scope="row" className="border border-border px-2 py-1 text-right font-normal text-muted-foreground whitespace-nowrap">
                                                  {table.index[ri]}
                                                </th>
                                                {row.map((cell, ci) => (
                                                  <td key={ci} className="border border-border px-2 py-1 whitespace-nowrap">
                                                    {cell}
                                                  </td>
                                                ))}
                                              </tr>
                                            ))}
                                          </tbody>
                                        </table>
                                      </div>
                                      {isPartial && (
                                        <p className="mt-1 text-[11px] text-muted-foreground">
                                          {t("tablePartial", { rows: table.rows.length, cols: table.columns.length })}
                                        </p>
                                      )}
                                    </td>
                                  </tr>
                                )}
                              </Fragment>
                            );
                          })}
                        </tbody>
                      </table>
                    )}
                  </div>
                );
              })}
            </div>
            <div className="mt-4">
              <div className="mb-1 text-xs font-bold text-muted-foreground">{t("output")}</div>
              <pre className="min-h-10 whitespace-pre-wrap rounded-lg border border-border bg-code p-2 font-mono text-xs">{output || " "}</pre>
              {atEnd && result.error && (
                <pre className="mt-2 whitespace-pre-wrap rounded-lg border border-danger/20 bg-danger-soft p-2 font-mono text-xs text-danger">
                  {result.error.type}: {result.error.message}
                </pre>
              )}
              {atEnd && result.truncated && <p className="mt-2 text-xs text-warning-ink">{t("truncated", { count: steps.length })}</p>}
            </div>
          </div>
        </div>
      )}

      {steps.length > 0 && (
        <div className="flex flex-wrap items-center gap-2 border-t px-4 py-3">
          <Button variant="ghost" size="icon-sm" onClick={() => go(0)} disabled={index === 0} aria-label={t("first")}>
            <ChevronFirst aria-hidden="true" />
          </Button>
          <Button variant="outline" size="sm" onClick={() => go(index - 1)} disabled={index === 0}>
            <ChevronLeft aria-hidden="true" /> {t("back")}
          </Button>
          <Button size="sm" onClick={() => setPlaying((p) => !p)} disabled={atEnd && !playing}>
            {playing ? <Pause aria-hidden="true" /> : <Play aria-hidden="true" />}
            {playing ? t("pause") : t("play")}
          </Button>
          <Button variant="outline" size="sm" onClick={() => go(index + 1)} disabled={atEnd}>
            {t("forward")} <ChevronRight aria-hidden="true" />
          </Button>
          <Button variant="ghost" size="icon-sm" onClick={() => go(last)} disabled={atEnd} aria-label={t("last")}>
            <ChevronLast aria-hidden="true" />
          </Button>
          <input
            type="range"
            min={0}
            max={last}
            value={index}
            onChange={(e) => go(Number(e.target.value))}
            aria-label={t("slider")}
            className="ml-2 min-w-32 flex-1 accent-[var(--primary)]"
          />
          <span className="hidden text-xs text-muted-foreground sm:inline">{t("keys")}</span>
        </div>
      )}
    </>
  );
}
