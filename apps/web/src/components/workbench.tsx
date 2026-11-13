"use client";

import { CheckCircle2, CircleDashed, FlaskConical, Loader2, Play, RotateCcw, Square, Terminal, Trash2, XCircle } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { CodeEditor } from "@/components/code-editor";
import { Button } from "@/components/ui/button";
import { CountUp } from "@/components/count-up";
import { Tooltip } from "@/components/ui/tooltip";
import { python, usePythonStatus } from "@/lib/python";
import type { TestRunResult } from "@/lib/types";
import { cn } from "@/lib/utils";

type OutLine = { text: string; stream: "stdout" | "stderr" | "error" | "info" };

export function PythonStatus() {
  const status = usePythonStatus();
  const t = useTranslations("editor");
  const label =
    status === "loading"
      ? t("pyLoading")
      : status === "error"
        ? t("pyError")
        : status === "idle"
          ? t("pyIdle")
          : t("pyReady", { version: python?.version ?? "" });
  return (
    <Tooltip content={label}>
      <span className="inline-flex items-center gap-1.5 text-xs text-muted-foreground">
        <span
          className={cn(
            "size-2 rounded-full",
            status === "ready" && "bg-primary",
            status === "running" && "bg-primary animate-pulse",
            status === "loading" && "bg-warning animate-pulse",
            status === "error" && "bg-danger",
            status === "idle" && "bg-muted-foreground/40",
          )}
          aria-hidden="true"
        />
        <span className="hidden sm:inline">{status === "loading" ? t("pyLoading") : "Python"}</span>
      </span>
    </Tooltip>
  );
}

export interface WorkbenchProps {
  code: string;
  onCodeChange: (code: string) => void;
  tests?: string;
  onTestResult?: (result: TestRunResult) => void;
  onReset?: () => void;
  highlightBlanks?: boolean;
  title?: React.ReactNode;
  className?: string;
}

export function Workbench({ code, onCodeChange, tests, onTestResult, onReset, highlightBlanks, title, className }: WorkbenchProps) {
  const t = useTranslations("editor");
  const te = useTranslations("exercise");
  const status = usePythonStatus();
  const [output, setOutput] = useState<OutLine[]>([]);
  const [result, setResult] = useState<TestRunResult | null>(null);
  const [panel, setPanel] = useState<"output" | "tests">("output");
  const [busy, setBusy] = useState<null | "run" | "check">(null);
  const [errorLine, setErrorLine] = useState<number | null>(null);

  useEffect(() => {
    python?.warmUp();
  }, []);

  // New exercise -> clear the old test results.
  useEffect(() => {
    setResult(null);
    setErrorLine(null);
    setPanel(tests ? "tests" : "output");
  }, [tests]);

  const run = async () => {
    if (busy) return;
    setBusy("run");
    setPanel("output");
    setErrorLine(null);
    setOutput([]);
    const res = await python.run(code, (text, stream) => setOutput((o) => [...o, { text, stream }]));
    if (res.timedOut) setOutput((o) => [...o, { text: t("timedOut"), stream: "error" }]);
    else if (res.stopped) setOutput((o) => [...o, { text: t("stopped"), stream: "info" }]);
    else if (!res.ok && res.error) {
      setOutput((o) => [...o, { text: res.error!, stream: "error" }]);
      const m = /line (\d+)/.exec(res.error.split("\n").reverse().find((l) => /File "main\.py", line \d+/.test(l)) ?? "");
      if (m) setErrorLine(Number(m[1]));
    } else setOutput((o) => [...o, { text: `✓ ${t("finished")}`, stream: "info" }]);
    setBusy(null);
  };

  const check = async () => {
    if (busy || !tests) return;
    setBusy("check");
    setPanel("tests");
    setErrorLine(null);
    const res = await python.test(code, tests);
    setResult(res);
    setErrorLine(res.error?.line ?? null);
    onTestResult?.(res);
    setBusy(null);
  };

  const stop = () => python.restart({ stopped: true });

  return (
    <div className={cn("flex min-h-0 flex-col bg-code", className)}>
      <div className="flex h-11 items-center gap-2 border-b border-border bg-code px-3 py-1.5">
        <div className="min-w-0 flex-1 truncate text-sm font-medium">{title}</div>
        <PythonStatus />
        {onReset && (
          <Tooltip content={te("reset")}>
            <Button variant="ghost" size="icon-sm" onClick={onReset} aria-label={te("reset")}>
              <RotateCcw aria-hidden="true" />
            </Button>
          </Tooltip>
        )}
        {busy ? (
          <Button variant="outline" size="sm" onClick={stop}>
            <Square className="fill-current" aria-hidden="true" />
            {t("stop")}
          </Button>
        ) : null}
        <Tooltip content={t("shortcutRun")}>
          <Button variant={tests ? "outline" : "default"} size="sm" onClick={run} disabled={!!busy}>
            {busy === "run" ? <Loader2 className="animate-spin" aria-hidden="true" /> : <Play aria-hidden="true" />}
            {t("run")}
          </Button>
        </Tooltip>
        {tests && (
          <Tooltip content={t("shortcutCheck")}>
            <Button size="sm" onClick={check} disabled={!!busy}>
              {busy === "check" ? <Loader2 className="animate-spin" aria-hidden="true" /> : <FlaskConical aria-hidden="true" />}
              {t("check")}
            </Button>
          </Tooltip>
        )}
      </div>

      <CodeEditor
        value={code}
        onChange={onCodeChange}
        onRun={run}
        onCheck={tests ? check : run}
        errorLine={errorLine}
        highlightBlanks={highlightBlanks}
        className="min-h-[220px] flex-1"
      />

      <div className="flex h-[38%] min-h-[170px] flex-col border-t border-border bg-code">
        <div className="flex items-center gap-1 border-b border-border/50 px-2 py-1.5">
          <PanelTab active={panel === "output"} onClick={() => setPanel("output")} icon={<Terminal className="size-3.5" />}>
            {t("output")}
          </PanelTab>
          {tests && (
            <PanelTab active={panel === "tests"} onClick={() => setPanel("tests")} icon={<FlaskConical className="size-3.5" />}>
              {t("tests")}
              {result && !result.timedOut && (
                <span className={cn("ml-1 rounded-full px-1.5 py-0.2 font-mono text-xs font-bold", result.ok ? "bg-success-soft text-primary-ink" : "bg-danger-soft text-danger")}>
                  {result.passed}/{result.total || "!"}
                </span>
              )}
            </PanelTab>
          )}
          {panel === "output" && output.length > 0 && (
            <button
              type="button"
              onClick={() => setOutput([])}
              aria-label={t("clear")}
              className="ml-auto inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
            >
              <Trash2 className="size-3.5" aria-hidden="true" />
              <span>{t("clear")}</span>
            </button>
          )}
        </div>
        <div className="min-h-0 flex-1 overflow-auto px-3 py-2 font-mono text-[13px]" aria-live="polite">
          {panel === "output" ? (
            output.length === 0 ? (
              <p className="font-sans text-sm text-muted-foreground">{status === "loading" ? t("pyLoading") : t("noOutput")}</p>
            ) : (
              output.map((l, i) => (
                <pre
                  key={i}
                  className={cn(
                    "whitespace-pre-wrap break-words font-mono text-[13px]",
                    l.stream === "stderr" && "text-warning-ink",
                    l.stream === "error" && "mt-1 rounded-md border border-danger/20 bg-danger-soft p-2 text-danger",
                    l.stream === "info" && "mt-1 font-sans text-xs text-muted-foreground",
                  )}
                >
                  {l.text}
                </pre>
              ))
            )
          ) : (
            <TestResults result={result} busy={busy === "check"} />
          )}
        </div>
      </div>
    </div>
  );
}

function PanelTab({ active, onClick, icon, children }: { active: boolean; onClick: () => void; icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "hit inline-flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring",
        active ? "bg-accent text-primary font-bold" : "text-muted-foreground hover:bg-muted/50 hover:text-foreground",
      )}
    >
      <span aria-hidden="true">{icon}</span>
      {children}
    </button>
  );
}

function TestResults({ result, busy }: { result: TestRunResult | null; busy: boolean }) {
  const t = useTranslations("editor");
  if (busy) {
    return (
      <p className="flex items-center gap-2 font-sans text-sm text-muted-foreground">
        <Loader2 className="size-4 animate-spin text-primary" aria-hidden="true" />
        {t("checking")}
      </p>
    );
  }
  if (!result) return <p className="font-sans text-sm text-muted-foreground">{t("noTests")}</p>;
  if (result.timedOut) {
    return (
      <div className="flex items-center gap-2 rounded-md border border-danger/20 bg-danger-soft p-2 font-sans text-sm text-danger">
        <XCircle className="size-4 shrink-0" aria-hidden="true" />
        <span>{t("timedOut")}</span>
      </div>
    );
  }
  if (result.error) {
    const blank = /name '___' is not defined/.test(result.error.message);
    return (
      <div className="space-y-2 font-sans">
        <div className="flex items-center gap-2 text-sm font-bold text-danger">
          <XCircle className="size-4 shrink-0" aria-hidden="true" />
          <span>{t("importError")}</span>
          {result.error.line ? <span className="font-normal text-muted-foreground">· {t("line", { line: result.error.line })}</span> : null}
        </div>
        <pre className="whitespace-pre-wrap rounded-md border border-danger/20 bg-danger-soft p-2 font-mono text-[13px] text-danger">
          {result.error.type}: {result.error.message}
        </pre>
        {blank && (
          <p className="rounded-md border border-warning/30 bg-warning-soft p-2 text-sm text-warning-ink">
            {t("blankHint")}
          </p>
        )}
      </div>
    );
  }
  return (
    <div className="space-y-2 font-sans">
      <div className="mb-3 flex flex-wrap items-center gap-x-5 gap-y-2 border-b border-border/50 pb-2">
        <div className="flex items-baseline gap-1">
          <span className={cn("font-mono text-3xl font-bold tabular-nums", result.ok ? "text-primary" : "text-foreground")}>
            <CountUp value={result.passed} />
          </span>
          <span className="font-mono text-sm font-bold text-muted-foreground tabular-nums">/{result.total}</span>
        </div>
        <div className="flex min-w-24 flex-1 flex-wrap gap-1" aria-hidden="true">
          {result.tests.map((tc, i) => (
            <span
              key={tc.name}
              style={{ animationDelay: `${i * 70}ms` }}
              className={cn(
                "animate-rise h-2.5 w-4 rounded-full border",
                tc.status === "passed" ? "border-primary bg-primary" : "border-danger bg-danger",
              )}
            />
          ))}
        </div>
        {result.ok && <span className="text-sm font-bold text-primary">{t("levelClear")}</span>}
        <div className={cn("flex w-full items-center gap-2 text-sm font-bold", result.ok ? "text-primary-ink" : "text-foreground")}>
          {result.ok ? <CheckCircle2 className="size-4 text-primary" aria-hidden="true" /> : <CircleDashed className="size-4 text-muted-foreground" aria-hidden="true" />}
          {result.ok ? t("allPassed") : t("testsPassed", { passed: result.passed, total: result.total })}
        </div>
      </div>
      <div className="space-y-1.5">
        {result.tests.map((tc) => (
          <div key={tc.name} className="animate-rise rounded-md border border-border/50 bg-card/50 p-2 text-sm">
            <div className="flex items-start gap-2">
              {tc.status === "passed" ? (
                <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true" />
              ) : (
                <XCircle className="mt-0.5 size-4 shrink-0 text-danger" aria-hidden="true" />
              )}
              <span className={cn("font-medium", tc.status === "passed" ? "text-muted-foreground" : "text-danger font-bold")}>
                {tc.label}
              </span>
            </div>
            {tc.message && (
              <pre className="ml-6 mt-1 whitespace-pre-wrap rounded-md bg-muted p-2 font-mono text-[13px] text-foreground">
                {tc.message}
              </pre>
            )}
          </div>
        ))}
      </div>
      {result.stdout.trim() && (
        <details className="mt-3 text-xs text-muted-foreground">
          <summary className="cursor-pointer font-medium hover:text-foreground">{t("stdoutDuringTests")}</summary>
          <pre className="mt-1 whitespace-pre-wrap rounded-md bg-muted/40 p-2 font-mono text-[13px]">{result.stdout}</pre>
        </details>
      )}
    </div>
  );
}
