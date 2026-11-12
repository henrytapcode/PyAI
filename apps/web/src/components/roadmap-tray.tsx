"use client";

import { Check } from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { catalog, phaseOfLesson } from "@/lib/content";
import { useLoc } from "@/lib/i18n";
import { useProgress } from "@/lib/progress";
import { lessonStatus, phaseProgress, type LessonStatus } from "@/lib/selectors";
import { cn, percent } from "@/lib/utils";

/**
 * Static map of the 7 phase tint background classes defined in tokens.css.
 * Phase order mapping:
 * - Order 0..6 -> tint 1..7 via order % 7
 * - Order 7, 8 -> cycle back to tint 1, 2 via order % 7
 */
const PHASE_TINT_CLASSES = [
  "bg-[var(--phase-1)]",
  "bg-[var(--phase-2)]",
  "bg-[var(--phase-3)]",
  "bg-[var(--phase-4)]",
  "bg-[var(--phase-5)]",
  "bg-[var(--phase-6)]",
  "bg-[var(--phase-7)]",
] as const;

export function getPhaseTintClass(order: number): string {
  return PHASE_TINT_CLASSES[order % 7];
}

export function trayCellClass(status: LessonStatus, isNext: boolean): string {
  if (isNext) {
    return "border-2 border-primary bg-card text-primary font-bold";
  }
  switch (status) {
    case "completed":
      return "border border-transparent bg-success-soft text-primary-ink";
    case "in_progress":
      return "border border-primary/50 bg-card text-foreground";
    case "available":
      return "border border-border bg-card/80 text-foreground";
    case "coming_soon":
      return "border border-dashed border-border bg-card/30 text-foreground opacity-60";
    case "skipped":
      return "border border-border bg-muted/60 text-foreground opacity-60";
    case "locked":
    default:
      return "border border-border bg-card/40 text-foreground opacity-60";
  }
}

export interface RoadmapTrayProps {
  variant: "compact" | "full";
  nextId?: string;
  className?: string;
}

export function RoadmapTray({ variant, nextId, className }: RoadmapTrayProps) {
  const ts = useTranslations("status");
  const tc = useTranslations("common");
  const loc = useLoc();
  const p = useProgress();

  const activePhaseId = nextId ? phaseOfLesson(nextId)?.id : undefined;

  return (
    <div className={cn("space-y-2", className)}>
      {catalog.phases.map((ph) => {
        const prog = phaseProgress(p, ph);
        const isOpen = variant === "full" || (activePhaseId !== undefined && ph.id === activePhaseId);
        const tintClass = getPhaseTintClass(ph.order);
        const pctValue = prog.skipped ? 1 : prog.fraction;
        const pctText = prog.ready > 0 ? percent(pctValue) : "";

        return (
          <div key={ph.id} className={cn("rounded-lg p-3", tintClass)}>
            {isOpen ? (
              <div>
                <div className="mb-2.5 flex items-center justify-between gap-3">
                  <div className="flex min-w-0 items-center gap-2">
                    <span className={cn("truncate text-sm font-bold text-foreground", !prog.ready && "opacity-60")}>
                      {loc.t(ph.title)}
                    </span>
                    {prog.skipped && <Badge variant="muted">{ts("skipped")}</Badge>}
                    {!prog.ready && (
                      <Badge variant="outline">
                        {tc("comingSoon")}
                      </Badge>
                    )}
                  </div>
                  {prog.ready > 0 && pctText && (
                    <span className="shrink-0 font-mono text-xs font-bold tabular-nums text-foreground">
                      {pctText}
                    </span>
                  )}
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {ph.lessons.map((l) => {
                    const st: LessonStatus = lessonStatus(p, { ...l, phaseId: ph.id });
                    const isNext = l.id === nextId;
                    const label = `${loc.t(l.title)}: ${ts(st)}`;

                    return (
                      <Link
                        key={l.id}
                        href={l.ready ? `/lesson/${l.id}/` : "/learn/"}
                        title={label}
                        aria-label={label}
                        className={cn(
                          "relative grid size-9 place-items-center rounded-md font-mono text-xs tabular-nums outline-none transition-[color,background-color,border-color,transform] duration-150 hover:-translate-y-0.5 active:translate-y-0 motion-reduce:transform-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring after:absolute after:-inset-1 after:content-['']",
                          trayCellClass(st, isNext),
                        )}
                      >
                        {st === "completed" ? (
                          <Check className="size-4" aria-hidden="true" />
                        ) : (
                          <span>{l.order}</span>
                        )}
                      </Link>
                    );
                  })}
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-between gap-3">
                <div className="flex min-w-0 items-center gap-2">
                  <span className={cn("truncate text-sm font-bold text-foreground", !prog.ready && "opacity-60")}>
                    {loc.t(ph.title)}
                  </span>
                  {prog.skipped && <Badge variant="muted">{ts("skipped")}</Badge>}
                  {!prog.ready && (
                    <Badge variant="outline">
                      {tc("comingSoon")}
                    </Badge>
                  )}
                </div>
                {prog.ready > 0 && (
                  <div className="flex shrink-0 items-center gap-2.5">
                    <Progress value={pctValue} className="w-16 sm:w-24" />
                    <span className="w-9 text-right font-mono text-xs font-bold tabular-nums text-foreground">
                      {pctText}
                    </span>
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
