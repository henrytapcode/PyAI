"use client";

import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { Workbench } from "@/components/workbench";
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
};

const KEY = "pyai-playground";

export default function PlaygroundPage() {
  const t = useTranslations("editor");
  const [code, setCode] = useState(TEMPLATES.hello);

  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(KEY);
      if (saved) setCode(saved);
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

  return (
    <div className="flex h-[calc(100dvh-3.5rem-4rem)] flex-col lg:h-dvh">
      <div className="flex flex-wrap items-center gap-3 border-b px-4 py-3 sm:px-6">
        <div className="min-w-0 flex-1">
          <h1 className="font-semibold">{t("playgroundTitle")}</h1>
          <p className="truncate text-xs text-muted-foreground">{t("playgroundSubtitle")}</p>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-xs text-muted-foreground">{t("templates")}:</span>
          {Object.keys(TEMPLATES).map((k) => (
            <button
              key={k}
              onClick={() => update(TEMPLATES[k])}
              className={cn("rounded-md border px-2 py-1 font-mono text-xs hover:bg-muted", code === TEMPLATES[k] && "border-primary text-primary")}
            >
              {k}
            </button>
          ))}
        </div>
      </div>
      <Workbench code={code} onCodeChange={update} title={<span className="font-mono text-muted-foreground">playground.py</span>} className="min-h-0 flex-1" />
    </div>
  );
}
