"use client";

import { ChevronFirst, ChevronLast, ChevronLeft, ChevronRight, Eye, Loader2, Pause, Play } from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog";
import { python } from "@/lib/python";
import type { TraceResult, TraceStep } from "@/lib/types";
import { cn } from "@/lib/utils";

type VisualizerState = { code: string } | null;

let openVisualizer: ((code: string) => void) | null = null;

/** Open the step-through view for a piece of code from anywhere (a lesson block, the editor...). */
export function visualize(code: string) {
  openVisualizer?.(code);
}

/** Mounted once (in the app shell). Renders the dialog when `visualize()` is called. */
export function VisualizerHost() {
  const [state, setState] = useState<VisualizerState>(null);
  useEffect(() => {
    openVisualizer = (code) => setState({ code });
    return () => {
      openVisualizer = null;
    };
  }, []);
  return (
    <Dialog open={!!state} onOpenChange={(o) => !o && setState(null)}>
      <DialogContent className="flex h-[min(88dvh,760px)] max-w-6xl flex-col gap-3 overflow-hidden p-0 sm:p-0">
        {state && <Visualizer key={state.code} code={state.code} />}
      </DialogContent>
    </Dialog>
  );
}

function Visualizer({ code }: { code: string }) {
  const t = useTranslations("visualize");
  const [result, setResult] = useState<TraceResult | null>(null);
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    let alive = true;
    python.trace(code).then((r) => {
      if (alive) setResult(r);
    });
    return () => {
      alive = false;
    };
  }, [code]);

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
  }, [go, index, last]);

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
        <Eye className="size-5 text-primary" />
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
            <Loader2 className="size-4 animate-spin" /> {t("tracing")}
          </span>
        </div>
      ) : result.timedOut ? (
        <p className="m-5 rounded-[4px] bg-danger-soft p-3 text-sm text-danger">{t("timedOut")}</p>
      ) : steps.length === 0 ? (
        <div className="m-5 space-y-2">
          {result.error ? (
            <pre className="whitespace-pre-wrap rounded-[4px] bg-danger-soft p-3 font-mono text-sm text-danger">
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
          <div className="min-h-0 overflow-auto border-b bg-code py-3 font-mono text-[13px] leading-6 md:border-b-0 md:border-r">
            {lines.map((text, i) => {
              const n = i + 1;
              const current = step?.line === n;
              const previous = !current && prev?.line === n;
              return (
                <div
                  key={n}
                  ref={current ? lineRef : undefined}
                  className={cn(
                    "flex gap-3 px-3",
                    current && (step?.event === "exception" ? "bg-danger-soft" : "bg-primary/15"),
                    previous && "bg-muted",
                  )}
                >
                  <span className="w-5 shrink-0 select-none text-right text-muted-foreground/70">{current ? "➜" : n}</span>
                  <span className="whitespace-pre">{text || " "}</span>
                </div>
              );
            })}
          </div>

          {/* State */}
          <div className="flex min-h-0 flex-col overflow-auto p-4">
            <p className={cn("mb-3 rounded-[4px] px-3 py-2 text-sm", step?.event === "exception" ? "bg-danger-soft text-danger" : "bg-accent/60")}>{caption}</p>
            <div className="space-y-3">
              {step?.stack.map((frame, fi) => {
                const before = prev?.stack[fi]?.name === frame.name ? prev.stack[fi] : undefined;
                return (
                  <div key={`${fi}-${frame.name}`} className={cn("rounded-[4px] border", fi === step.stack.length - 1 && "border-primary/50")}>
                    <div className="flex items-center gap-2 border-b px-3 py-1.5 text-xs font-bold">
                      {frame.name === "global" ? t("globals") : t("frame", { name: frame.name })}
                    </div>
                    {frame.vars.length === 0 ? (
                      <p className="px-3 py-2 text-xs text-muted-foreground">{t("noVars")}</p>
                    ) : (
                      <table className="w-full text-sm">
                        <tbody>
                          {frame.vars.map((v) => {
                            const old = before?.vars.find((x) => x.name === v.name);
                            const changed = !old || old.repr !== v.repr;
                            return (
                              <tr key={v.name} className={cn("border-b last:border-0", changed && index > 0 && "bg-warning-soft/70 transition-colors")}>
                                <td className="w-1/3 px-3 py-1.5 font-mono text-[13px] font-medium">{v.name}</td>
                                <td className="px-3 py-1.5 font-mono text-[13px] break-all">{v.repr}</td>
                                <td className="w-0 px-3 py-1.5 text-right">
                                  <Badge variant="muted" className="font-mono">
                                    {v.type}
                                  </Badge>
                                </td>
                              </tr>
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
              <pre className="min-h-10 whitespace-pre-wrap rounded-[4px] border bg-code p-2 font-mono text-[13px]">{output || " "}</pre>
              {atEnd && result.error && (
                <pre className="mt-2 whitespace-pre-wrap rounded-[4px] bg-danger-soft p-2 font-mono text-[13px] text-danger">
                  {result.error.type}: {result.error.message}
                </pre>
              )}
              {atEnd && result.truncated && <p className="mt-2 text-xs text-warning">{t("truncated", { count: steps.length })}</p>}
            </div>
          </div>
        </div>
      )}

      {steps.length > 0 && (
        <div className="flex flex-wrap items-center gap-2 border-t px-4 py-3">
          <Button variant="ghost" size="icon-sm" onClick={() => go(0)} disabled={index === 0} aria-label={t("first")}>
            <ChevronFirst />
          </Button>
          <Button variant="outline" size="sm" onClick={() => go(index - 1)} disabled={index === 0}>
            <ChevronLeft /> {t("back")}
          </Button>
          <Button size="sm" onClick={() => setPlaying((p) => !p)} disabled={atEnd && !playing}>
            {playing ? <Pause /> : <Play />}
            {playing ? t("pause") : t("play")}
          </Button>
          <Button variant="outline" size="sm" onClick={() => go(index + 1)} disabled={atEnd}>
            {t("forward")} <ChevronRight />
          </Button>
          <Button variant="ghost" size="icon-sm" onClick={() => go(last)} disabled={atEnd} aria-label={t("last")}>
            <ChevronLast />
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
