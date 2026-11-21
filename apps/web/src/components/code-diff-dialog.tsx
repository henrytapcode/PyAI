"use client";

import { DiffEditor } from "@monaco-editor/react";
import { CheckCircle2, Columns2, Rows2 } from "lucide-react";
import { useTranslations } from "next-intl";
import { useTheme } from "next-themes";
import * as React from "react";
import { useEffect, useState } from "react";
import { definePyaiThemes } from "@/components/code-editor";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog";
import { cn } from "@/lib/utils";

export interface DiffTarget {
  id: string;
  label: string;
  code: string;
}

export interface CodeDiffDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  exerciseTitle: string;
  userCode: string;
  targets: DiffTarget[];
  initialTargetId?: string;
  onLoadTarget?: (code: string) => void;
}

export function CodeDiffDialog({
  open,
  onOpenChange,
  exerciseTitle,
  userCode,
  targets,
  initialTargetId,
  onLoadTarget,
}: CodeDiffDialogProps): React.JSX.Element {
  const t = useTranslations("exercise");
  const te = useTranslations("editor");
  const { resolvedTheme } = useTheme();

  const [selectedId, setSelectedId] = useState<string>(() => initialTargetId ?? targets[0]?.id ?? "");
  const [sideBySide, setSideBySide] = useState<boolean>(true);

  useEffect(() => {
    if (open) {
      setSelectedId(initialTargetId ?? targets[0]?.id ?? "");
    }
  }, [open, initialTargetId, targets]);

  useEffect(() => {
    const mq = window.matchMedia("(min-width: 768px)");
    setSideBySide(mq.matches);
  }, []);

  const activeTarget = targets.find((target) => target.id === selectedId) ?? targets[0];
  const isIdentical = Boolean(activeTarget && userCode.trim() === activeTarget.code.trim());

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-5xl w-[calc(100%-2rem)] gap-0 overflow-hidden p-0">
        <div className="flex flex-col gap-3 border-b border-border px-4 py-4 pr-14 sm:flex-row sm:items-center sm:justify-between sm:px-6 sm:pr-14">
          <div className="min-w-0 space-y-1">
            <div className="flex flex-wrap items-center gap-2">
              <DialogTitle className="truncate">{t("diffTitle")}</DialogTitle>
              {isIdentical && (
                <Badge variant="success">
                  <CheckCircle2 aria-hidden="true" />
                  {t("identicalCode")}
                </Badge>
              )}
            </div>
            <DialogDescription className="truncate">
              {exerciseTitle} · {t("diffDescription")}
            </DialogDescription>
          </div>

          <div
            role="group"
            aria-label={t("diffTitle")}
            className="inline-flex shrink-0 items-center self-start rounded-md border border-border bg-muted p-0.5 sm:self-auto"
          >
            <button
              type="button"
              aria-pressed={sideBySide}
              onClick={() => setSideBySide(true)}
              className={cn(
                "hit relative inline-flex items-center gap-1.5 rounded-sm px-2.5 py-1 text-xs font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring",
                sideBySide ? "bg-card text-primary" : "text-muted-foreground hover:text-foreground",
              )}
            >
              <Columns2 className="size-3.5" aria-hidden="true" />
              {t("sideBySide")}
            </button>
            <button
              type="button"
              aria-pressed={!sideBySide}
              onClick={() => setSideBySide(false)}
              className={cn(
                "hit relative inline-flex items-center gap-1.5 rounded-sm px-2.5 py-1 text-xs font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring",
                !sideBySide ? "bg-card text-primary" : "text-muted-foreground hover:text-foreground",
              )}
            >
              <Rows2 className="size-3.5" aria-hidden="true" />
              {t("inlineDiff")}
            </button>
          </div>
        </div>

        {targets.length > 1 && (
          <div className="flex items-center gap-1.5 overflow-x-auto border-b border-border bg-muted/40 px-4 py-2 sm:px-6">
            {targets.map((target) => {
              const active = target.id === activeTarget?.id;
              return (
                <button
                  key={target.id}
                  type="button"
                  aria-pressed={active}
                  onClick={() => setSelectedId(target.id)}
                  className={cn(
                    "hit relative shrink-0 rounded-full border px-3 py-1 text-xs font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring",
                    active
                      ? "border-primary bg-accent text-primary"
                      : "border-border bg-card text-muted-foreground hover:bg-accent/50 hover:text-foreground",
                  )}
                >
                  {target.label}
                </button>
              );
            })}
          </div>
        )}

        {sideBySide && activeTarget && (
          <div className="grid grid-cols-2 border-b border-border bg-muted/60 text-xs font-medium text-muted-foreground">
            <div className="truncate border-r border-border px-4 py-1.5 sm:px-6">{t("yourCode")}</div>
            <div className="truncate px-4 py-1.5 sm:px-6">{activeTarget.label}</div>
          </div>
        )}

        <div className="h-[60vh] min-h-[320px] max-h-[680px] w-full bg-[var(--code-bg)]">
          {open && activeTarget && (
            <DiffEditor
              language="python"
              original={userCode}
              modified={activeTarget.code}
              beforeMount={definePyaiThemes}
              theme={resolvedTheme === "dark" ? "pyai-dark" : "pyai-light"}
              keepCurrentOriginalModel
              keepCurrentModifiedModel
              loading={<div className="grid h-full place-items-center text-sm text-muted-foreground">{te("loading")}</div>}
              options={{
                readOnly: true,
                originalEditable: false,
                renderSideBySide: sideBySide,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                automaticLayout: true,
                fontSize: 14,
                fontFamily: "var(--font-mono-face), 'JetBrains Mono', Consolas, monospace",
                fontLigatures: true,
                wordWrap: "on",
                padding: { top: 12, bottom: 12 },
                overviewRulerLanes: 0,
                scrollbar: { verticalScrollbarSize: 8, horizontalScrollbarSize: 8 },
              }}
            />
          )}
        </div>

        {onLoadTarget && activeTarget && (
          <div className="flex items-center justify-end gap-2 border-t border-border bg-card px-4 py-3 sm:px-6">
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                onLoadTarget(activeTarget.code);
                onOpenChange(false);
              }}
            >
              {t("loadSolution")}
            </Button>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
