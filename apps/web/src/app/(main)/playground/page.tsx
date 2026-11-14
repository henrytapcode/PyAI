"use client";

import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { Workbench } from "@/components/workbench";
import type { RunnerKind } from "@/lib/python";
import { cn } from "@/lib/utils";

const TEMPLATES: Record<string, string> = {
  hello: `name = "AI engineer"
for step in range(3):
    print(f"Step {step + 1}: hello, {name}!")
`,
  numpy: `import numpy as np

scores = np.array([7.5, 8.0, 9.25, 6.5])
print("mean:", scores.mean())
print("normalized:", (scores - scores.min()) / (scores.max() - scores.min()))
`,
  pandas: `import pandas as pd

df = pd.DataFrame({
    "model": ["baseline", "tuned", "rag"],
    "accuracy": [0.71, 0.78, 0.86],
    "latency_ms": [120, 135, 310],
})
print(df.sort_values("accuracy", ascending=False))
print(df.describe())
`,
  words: `text = "the model reads the text and the model learns"
counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1
for word, n in sorted(counts.items(), key=lambda kv: -kv[1]):
    print(f"{word:>8} {'#' * n}")
`,
  torch: `import torch

torch.manual_seed(0)
x = torch.randn(3, 2)
w = torch.ones(2, requires_grad=True)
loss = (x @ w).pow(2).mean()
loss.backward()
print("loss:", round(loss.item(), 3))
print("grad:", [round(g, 3) for g in w.grad.tolist()])
`,
};

const KEY = "pyai-playground";
const RUNNER_KEY = "pyai-playground-runner";

export default function PlaygroundPage() {
  const t = useTranslations("editor");
  const [code, setCode] = useState(TEMPLATES.hello);
  const [runner, setRunner] = useState<RunnerKind>("pyodide");

  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(KEY);
      if (saved) setCode(saved);
      const savedRunner = window.localStorage.getItem(RUNNER_KEY);
      if (savedRunner === "local" || savedRunner === "pyodide") setRunner(savedRunner);
    } catch {
      /* storage unavailable */
    }
  }, []);

  const update = (v: string) => {
    setCode(v);
    try {
      window.localStorage.setItem(KEY, v);
    } catch {
      /* storage unavailable */
    }
  };

  const updateRunner = (next: RunnerKind) => {
    setRunner(next);
    try {
      window.localStorage.setItem(RUNNER_KEY, next);
    } catch {
      /* storage unavailable */
    }
  };

  return (
    <div className="flex h-[calc(100dvh-3.5rem-4rem)] flex-col lg:h-dvh">
      <div className="flex shrink-0 flex-col gap-3 border-b border-border bg-muted px-4 py-3 sm:px-6 lg:flex-row lg:items-center lg:justify-between">
        <div className="min-w-0 flex-1 lg:min-w-56">
          <h1 className="text-lg font-bold tracking-tight">{t("playgroundTitle")}</h1>
          <p className="line-clamp-2 text-sm text-muted-foreground">{t("playgroundSubtitle")}</p>
        </div>
        <div className="flex flex-wrap items-center gap-3 lg:justify-end">
          <div
            role="group"
            aria-label={t("runnerLabel")}
            className="flex flex-wrap items-center gap-1.5"
          >
            <span className="text-sm text-muted-foreground">{t("runnerGroupLabel")}</span>
            {(["pyodide", "local"] as const).map((kind) => (
              <button
                key={kind}
                type="button"
                aria-pressed={runner === kind}
                onClick={() => updateRunner(kind)}
                className={cn(
                  "relative inline-flex h-9 items-center justify-center rounded-md border px-3 text-xs transition-colors",
                  "after:absolute after:-inset-1 after:content-['']",
                  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring",
                  runner === kind
                    ? "border-primary bg-accent font-bold text-primary"
                    : "border-border bg-card text-foreground hover:bg-accent",
                )}
              >
                {kind === "pyodide" ? t("runnerBrowser") : t("runnerLocal")}
              </button>
            ))}
          </div>
          <div
            role="group"
            aria-label={t("templates")}
            className="flex flex-wrap items-center gap-1.5"
          >
            <span className="text-sm text-muted-foreground">{t("templatesLabel")}</span>
            {Object.keys(TEMPLATES).map((k) => (
              <button
                key={k}
                type="button"
                aria-pressed={code === TEMPLATES[k]}
                onClick={() => {
                  update(TEMPLATES[k]);
                  if (k === "torch") updateRunner("local");
                }}
                className={cn(
                  "relative inline-flex h-9 items-center justify-center rounded-md border px-3 font-mono text-xs transition-colors",
                  "after:absolute after:-inset-1 after:content-['']",
                  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring",
                  code === TEMPLATES[k]
                    ? "border-primary bg-accent font-bold text-primary"
                    : "border-border bg-card text-foreground hover:bg-accent",
                )}
              >
                {k}
              </button>
            ))}
          </div>
        </div>
      </div>
      <Workbench
        code={code}
        onCodeChange={update}
        runner={runner}
        title={<span className="font-mono text-sm text-muted-foreground">playground.py</span>}
        className="min-h-0 flex-1"
      />
    </div>
  );
}
