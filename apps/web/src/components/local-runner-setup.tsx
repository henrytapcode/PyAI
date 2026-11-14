"use client";

import { Check, Copy, Loader2, RefreshCw, Terminal } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { localRunner, useLocalRunnerStatus } from "@/lib/local-runner";
import { cn } from "@/lib/utils";

const BASE_CMD = "uv run python tools/localrunner/serve.py";

function CommandBlock({ command }: { command: string }) {
  const tc = useTranslations("common");
  const t = useTranslations("localRunner");
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(command);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      /* clipboard blocked */
    }
  };

  return (
    <div className="flex items-center gap-2 rounded-md border border-border bg-code px-3 py-2">
      <code className="min-w-0 flex-1 overflow-x-auto whitespace-nowrap font-mono text-xs text-foreground">{command}</code>
      <button
        type="button"
        onClick={copy}
        aria-label={copied ? tc("copied") : t("copyCommand")}
        className="hit inline-flex shrink-0 items-center gap-1 rounded-md px-2 py-1 font-sans text-xs font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
      >
        {copied ? <Check className="size-3.5 text-primary" aria-hidden="true" /> : <Copy className="size-3.5" aria-hidden="true" />}
        <span>{copied ? tc("copied") : tc("copy")}</span>
      </button>
    </div>
  );
}

export function LocalRunnerSetup({
  onConnected,
  className,
}: {
  onConnected?: () => void;
  className?: string;
}) {
  const t = useTranslations("localRunner");
  const status = useLocalRunnerStatus();
  const [origin, setOrigin] = useState<string | null>(null);
  const checking = status === "checking";

  useEffect(() => {
    const o = window.location.origin;
    if (o !== "http://localhost:3000" && o !== "http://127.0.0.1:3000") {
      setOrigin(o);
    }
  }, []);

  const retry = async () => {
    const ok = await localRunner.check();
    if (ok) onConnected?.();
  };

  return (
    <div className={cn("space-y-3 rounded-lg border border-border bg-card p-4 font-sans text-sm", className)}>
      <div className="flex items-start gap-2.5">
        <Terminal className="mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true" />
        <div className="min-w-0 space-y-1">
          <h3 className="font-bold text-foreground">{t("title")}</h3>
          <p className="text-xs leading-relaxed text-muted-foreground">{t("description")}</p>
        </div>
      </div>

      <div className="space-y-1.5">
        <p className="text-xs text-muted-foreground">{t("runFromRoot")}</p>
        <CommandBlock command={BASE_CMD} />
      </div>

      {origin && (
        <div className="space-y-1.5">
          <p className="text-xs text-warning-ink">{t("originHint", { origin })}</p>
          <CommandBlock command={`${BASE_CMD} --allow-origin ${origin}`} />
        </div>
      )}

      <div>
        <Button type="button" size="sm" variant="outline" onClick={retry} disabled={checking}>
          {checking ? <Loader2 className="animate-spin" aria-hidden="true" /> : <RefreshCw aria-hidden="true" />}
          {checking ? t("checkingBtn") : t("retry")}
        </Button>
      </div>
    </div>
  );
}
