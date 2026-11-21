"use client";

import { Download, Eye, PenLine, Trash2 } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { Markdown } from "@/components/markdown";
import { Button } from "@/components/ui/button";
import { useProgress } from "@/lib/progress";
import { cn } from "@/lib/utils";

export function LessonNotes({
  lessonId,
  lessonTitle,
  onTryCode,
}: {
  lessonId: string;
  lessonTitle: string;
  onTryCode: (code: string) => void;
}) {
  const t = useTranslations("lesson");
  const tc = useTranslations("common");
  const saved = useProgress((s) => s.notes?.[lessonId]);
  const saveNote = useProgress((s) => s.saveNote);
  const deleteNote = useProgress((s) => s.deleteNote);

  const [mode, setMode] = useState<"edit" | "preview">("edit");
  const [draft, setDraft] = useState<string>(saved?.content ?? "");
  const [status, setStatus] = useState<"idle" | "saving" | "saved">("idle");
  const [confirmClear, setConfirmClear] = useState(false);

  const timerRef = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  const pendingRef = useRef<{ lessonId: string; content: string } | null>(null);

  // Flush any pending save for the previous lesson when switching lessons, then load the new draft.
  useEffect(() => {
    clearTimeout(timerRef.current);
    if (pendingRef.current && pendingRef.current.lessonId !== lessonId) {
      saveNote(pendingRef.current.lessonId, pendingRef.current.content);
      pendingRef.current = null;
    }
    setDraft(useProgress.getState().notes?.[lessonId]?.content ?? "");
    setStatus("idle");
    setConfirmClear(false);
  }, [lessonId, saveNote]);

  // Sync draft if persisted store hydrates after initial mount (e.g. direct ?tab=notes reload).
  useEffect(() => {
    if (!pendingRef.current && saved?.content !== undefined) {
      setDraft(saved.content);
    }
  }, [saved?.content]);

  // Flush any pending debounced save on unmount.
  useEffect(() => {
    return () => {
      clearTimeout(timerRef.current);
      if (pendingRef.current) {
        saveNote(pendingRef.current.lessonId, pendingRef.current.content);
        pendingRef.current = null;
      }
    };
  }, [saveNote]);

  const handleChange = (nextText: string) => {
    setDraft(nextText);
    setConfirmClear(false);
    setStatus("saving");
    clearTimeout(timerRef.current);
    pendingRef.current = { lessonId, content: nextText };
    timerRef.current = setTimeout(() => {
      saveNote(lessonId, nextText);
      pendingRef.current = null;
      setStatus("saved");
    }, 400);
  };

  const handleExport = () => {
    const blob = new Blob([`# ${lessonTitle}\n\n${draft}`], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${lessonId}-notes.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleConfirmClear = () => {
    clearTimeout(timerRef.current);
    pendingRef.current = null;
    setDraft("");
    deleteNote(lessonId);
    setConfirmClear(false);
    setStatus("idle");
  };

  const isEmpty = draft.trim().length === 0;

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="inline-flex items-center gap-1 rounded-md border border-border bg-muted p-1" role="group" aria-label={t("notes")}>
          <button
            type="button"
            aria-pressed={mode === "edit"}
            onClick={() => setMode("edit")}
            className={cn(
              "hit inline-flex items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition-colors",
              mode === "edit" ? "border border-border bg-card font-bold text-foreground" : "text-muted-foreground hover:text-foreground",
            )}
          >
            <PenLine className="size-3.5" aria-hidden="true" />
            {t("noteEdit")}
          </button>
          <button
            type="button"
            aria-pressed={mode === "preview"}
            onClick={() => setMode("preview")}
            className={cn(
              "hit inline-flex items-center gap-1.5 rounded-md px-3 py-1.5 text-xs font-medium transition-colors",
              mode === "preview" ? "border border-border bg-card font-bold text-foreground" : "text-muted-foreground hover:text-foreground",
            )}
          >
            <Eye className="size-3.5" aria-hidden="true" />
            {t("notePreview")}
          </button>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <span aria-live="polite" className="text-xs text-muted-foreground">
            {status === "saving" ? t("noteSaving") : status === "saved" ? t("noteSaved") : ""}
          </span>

          <Button variant="outline" size="sm" onClick={handleExport} disabled={isEmpty}>
            <Download aria-hidden="true" />
            {t("noteExport")}
          </Button>

          {confirmClear ? (
            <div className="flex items-center gap-1.5">
              <Button variant="danger" size="sm" onClick={handleConfirmClear}>
                {t("noteClearConfirm")}
              </Button>
              <Button variant="ghost" size="sm" onClick={() => setConfirmClear(false)}>
                {tc("cancel")}
              </Button>
            </div>
          ) : (
            <Button variant="ghost" size="sm" onClick={() => setConfirmClear(true)} disabled={isEmpty}>
              <Trash2 aria-hidden="true" />
              {t("noteClear")}
            </Button>
          )}
        </div>
      </div>

      {mode === "edit" ? (
        <div className="space-y-2">
          <textarea
            value={draft}
            onChange={(e) => handleChange(e.target.value)}
            aria-label={t("notes")}
            placeholder={t("notePlaceholder")}
            className="min-h-[320px] w-full resize-y rounded-lg border border-border bg-card p-4 font-mono text-sm leading-relaxed text-foreground placeholder:text-muted-foreground focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
          />
          <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-muted-foreground">
            <span>{t("noteHint")}</span>
            <span className="font-mono tabular-nums">{t("noteChars", { count: draft.length })}</span>
          </div>
        </div>
      ) : !isEmpty ? (
        <div className="rounded-lg border border-border bg-card p-5">
          <Markdown text={draft} onTryCode={onTryCode} canVisualize={false} />
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center gap-3 rounded-lg border border-border bg-card p-8 text-center">
          <p className="text-sm text-muted-foreground">{t("noteEmptyPreview")}</p>
          <Button variant="outline" size="sm" onClick={() => setMode("edit")}>
            <PenLine aria-hidden="true" />
            {t("noteEdit")}
          </Button>
        </div>
      )}
    </div>
  );
}
