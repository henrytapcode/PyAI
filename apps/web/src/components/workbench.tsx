"use client";

import { CheckCircle2, CircleDashed, FlaskConical, Loader2, Play, RotateCcw, Square, Terminal, Trash2, XCircle } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { CodeEditor } from "@/components/code-editor";
import { Button } from "@/components/ui/button";
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
            "size-2 rounded-[2px]",
            status === "ready" && "bg-success",
            status === "running" && "bg-primary animate-pulse",
            status === "loading" && "bg-warning animate-pulse",
            status === "error" && "bg-danger",
            status === "idle" && "bg-muted-foreground/40",
          )}
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
    <div className={cn("flex min-h-0 flex-col bg-card", className)}>
      <div className="flex items-center gap-2 border-b px-3 py-2">
        <div className="min-w-0 flex-1 truncate text-sm font-medium">{title}</div>
        <PythonStatus />
        {onReset && (
          <Tooltip content={te("reset")}>
            <Button variant="ghost" size="icon-sm" onClick={onReset} aria-label={te("reset")}>
              <RotateCcw />
            </Button>
          </Tooltip>
        )}
        {busy ? (
          <Button variant="outline" size="sm" onClick={stop}>
            <Square className="fill-current" />
            {t("stop")}
          </Button>
        ) : null}
        <Tooltip content={t("shortcutRun")}>
          <Button variant={tests ? "outline" : "default"} size="sm" onClick={run} disabled={!!busy}>
            {busy === "run" ? <Loader2 className="animate-spin" /> : <Play />}
            {t("run")}
          </Button>
        </Tooltip>
        {tests && (
          <Tooltip content={t("shortcutCheck")}>
            <Button size="sm" onClick={check} disabled={!!busy}>
              {busy === "check" ? <Loader2 className="animate-spin" /> : <FlaskConical />}
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

      <div className="flex h-[38%] min-h-[170px] flex-col border-t">
        <div className="flex items-center gap-1 px-2 pt-1.5">
          <PanelTab active={panel === "output"} onClick={() => setPanel("output")} icon={<Terminal className="size-3.5" />}>
            {t("output")}
          </PanelTab>
          {tests && (
            <PanelTab active={panel === "tests"} onClick={() => setPanel("tests")} icon={<FlaskConical className="size-3.5" />}>
              {t("tests")}
              {result && !result.timedOut && (
                <span className={cn("ml-1 rounded-[2px] px-1.5 text-[10px] font-bold", result.ok ? "bg-success-soft text-success" : "bg-danger-soft text-danger")}>
                  {result.passed}/{result.total || "!"}
                </span>
              )}
            </PanelTab>
          )}
          {panel === "output" && output.length > 0 && (
            <button onClick={() => setOutput([])} className="ml-auto inline-flex items-center gap-1 rounded-[2px] px-2 py-1 text-xs text-muted-foreground hover:bg-muted">
              <Trash2 className="size-3.5" />
              {t("clear")}
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
                    "whitespace-pre-wrap break-words",
                    l.stream === "stderr" && "text-warning",
                    l.stream === "error" && "mt-1 rounded-[2px] bg-danger-soft p-2 text-danger",
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
      onClick={onClick}
      className={cn(
        "inline-flex items-center gap-1.5 rounded-[2px] px-2.5 py-1 text-xs font-medium",
        active ? "bg-muted text-foreground" : "text-muted-foreground hover:text-foreground",
      )}
    >
      {icon}
      {children}
    </button>
  );
}

function TestResults({ result, busy }: { result: TestRunResult | null; busy: boolean }) {
  const t = useTranslations("editor");
  if (busy) {
    return (
      <p className="flex items-center gap-2 font-sans text-sm text-muted-foreground">
        <Loader2 className="size-4 animate-spin" />
        {t("checking")}
      </p>
    );
  }
  if (!result) return <p className="font-sans text-sm text-muted-foreground">{t("noTests")}</p>;
  if (result.timedOut) return <p className="rounded-[2px] bg-danger-soft p-2 font-sans text-sm text-danger">{t("timedOut")}</p>;
  if (result.error) {
    const blank = /name '___' is not defined/.test(result.error.message);
    return (
      <div className="space-y-2 font-sans">
        <div className="flex items-center gap-2 text-sm font-bold text-danger">
          <XCircle className="size-4" />
          {t("importError")}
          {result.error.line ? <span className="font-normal text-muted-foreground">· {t("line", { line: result.error.line })}</span> : null}
        </div>
        <pre className="whitespace-pre-wrap rounded-[2px] bg-danger-soft p-2 font-mono text-[13px] text-danger">
          {result.error.type}: {result.error.message}
        </pre>
        {blank && <p className="text-sm text-warning">{t("blankHint")}</p>}
      </div>
    );
  }
  return (
    <div className="space-y-1.5 font-sans">
      <div className={cn("mb-2 flex items-center gap-2 text-sm font-bold", result.ok ? "text-success" : "text-foreground")}>
        {result.ok ? <CheckCircle2 className="size-4" /> : <CircleDashed className="size-4 text-muted-foreground" />}
        {result.ok ? t("allPassed") : t("testsPassed", { passed: result.passed, total: result.total })}
      </div>
      {result.tests.map((tc) => (
        <div key={tc.name} className="animate-rise">
          <div className="flex items-start gap-2 text-sm">
            {tc.status === "passed" ? (
              <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-success" />
            ) : (
              <XCircle className="mt-0.5 size-4 shrink-0 text-danger" />
            )}
            <span className={tc.status === "passed" ? "text-muted-foreground" : ""}>{tc.label}</span>
          </div>
          {tc.message && <pre className="ml-6 mt-1 whitespace-pre-wrap rounded-[2px] bg-muted p-2 font-mono text-[12.5px] text-foreground/90">{tc.message}</pre>}
        </div>
      ))}
      {result.stdout.trim() && (
        <details className="mt-3 text-xs text-muted-foreground">
          <summary className="cursor-pointer">{t("stdoutDuringTests")}</summary>
          <pre className="mt-1 whitespace-pre-wrap font-mono">{result.stdout}</pre>
        </details>
      )}
    </div>
  );
}
