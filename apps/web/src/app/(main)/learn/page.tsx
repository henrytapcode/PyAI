"use client";

import { ArrowRight, BookOpen, Check, ClipboardCheck, Clock, Cpu, FolderGit2, Lock, Trophy } from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { useEffect } from "react";
import { PageHeader } from "@/components/page-header";
import { PhaseIcon } from "@/components/phase-icon";
import { getPhaseTintClass, trayCellClass } from "@/components/roadmap-tray";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { capstones, catalog, findLesson } from "@/lib/content";
import { Tx, useLoc } from "@/lib/i18n";
import { useProgress } from "@/lib/progress";
import { isLessonComplete, lessonParts, lessonStatus, nextLesson, phaseProgress } from "@/lib/selectors";
import { cn, percent } from "@/lib/utils";

export default function LearnPage() {
  const t = useTranslations("learn");
  const tc = useTranslations("common");
  const ts = useTranslations("status");
  const loc = useLoc();
  const p = useProgress();
  const placement = catalog.exams.find((e) => e.kind === "placement");
  const next = nextLesson(p);

  // Level select: j/k move between lessons; arrows do too once a row has focus. Enter opens it.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const el = e.target as HTMLElement | null;
      if (e.metaKey || e.ctrlKey || e.altKey || (el instanceof HTMLElement && el.closest("input, textarea, select, [contenteditable=true]"))) return;
      const rows = Array.from(document.querySelectorAll<HTMLAnchorElement>("a[data-lesson-row]"));
      if (!rows.length) return;
      const at = rows.indexOf(document.activeElement as HTMLAnchorElement);
      const down = e.key === "j" || (e.key === "ArrowDown" && at >= 0);
      const up = e.key === "k" || (e.key === "ArrowUp" && at >= 0);
      if (!down && !up) return;
      e.preventDefault();
      const start = at >= 0 ? at : Math.max(0, rows.findIndex((r) => r.dataset.live === "true"));
      const to = at < 0 ? start : Math.min(rows.length - 1, Math.max(0, at + (down ? 1 : -1)));
      rows[to].focus();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <div>
      <PageHeader display title={t("title")} subtitle={t("subtitle")} />

      {p.profile.track === "B" && !p.placement && placement && (
        <Card className="mb-8 flex flex-wrap items-center gap-4 bg-accent p-5">
          <Trophy className="size-6 shrink-0 text-primary" aria-hidden="true" />
          <p className="flex-1 text-sm text-foreground">{t("trackB")}</p>
          <Button asChild size="sm">
            <Link href="/placement/">{t("takePlacement")}</Link>
          </Button>
        </Card>
      )}

      <ol className="relative space-y-6">
        {catalog.phases.map((phase) => {
          const prog = phaseProgress(p, phase);
          const hasContent = prog.ready > 0;
          const pctValue = prog.skipped ? 1 : prog.fraction;
          const tintClass = getPhaseTintClass(phase.order);

          return (
            <li key={phase.id} className={cn("rounded-lg p-3 sm:p-4", tintClass)}>
              <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span aria-hidden="true" className="shrink-0">
                      <PhaseIcon name={phase.icon} className="size-5 text-foreground" />
                    </span>
                    <h2 className="text-lg font-bold text-foreground">
                      <span className="mr-2 text-sm font-medium">{t("phase", { n: phase.order })}</span>
                      <Tx value={phase.title} />
                    </h2>
                  </div>
                  {phase.summary && (
                    <p className="mt-1 text-sm text-foreground/80">{loc.t(phase.summary)}</p>
                  )}
                </div>

                <div className="flex flex-col items-start gap-2 sm:items-end sm:shrink-0">
                  <div className="flex flex-wrap gap-1.5 sm:justify-end">
                    {phase.lessons.some((l) => l.runner === "local") && (
                      <Badge variant="outline" className="border-foreground/25 text-foreground">
                        <Cpu className="size-3.5" aria-hidden="true" /> {t("localRunner")}
                      </Badge>
                    )}
                    {prog.skipped && <Badge variant="muted" className="border-foreground/25 text-foreground">{ts("skipped")}</Badge>}
                    {!hasContent && <Badge variant="outline" className="border-foreground/25 text-foreground">{tc("comingSoon")}</Badge>}
                  </div>
                  {hasContent && (
                    <div className="flex w-full items-center gap-2 sm:w-40">
                      <Progress value={pctValue} className="flex-1" />
                      <span className="shrink-0 font-mono text-xs font-bold tabular-nums text-foreground">
                        {percent(pctValue)}
                      </span>
                    </div>
                  )}
                </div>
              </div>

              <ul className="mt-3.5 divide-y divide-border overflow-hidden rounded-md bg-card/70">
                {phase.lessons.map((l) => {
                  const st = lessonStatus(p, { ...l, phaseId: phase.id });
                  const isNext = l.id === next?.id;
                  const parts = l.ready ? lessonParts(p, l) : null;
                  const missing = l.prerequisites.filter(
                    (pre) => !phase.lessons.some((x) => x.id === pre) || st === "locked",
                  );

                  const cell = (
                    <div
                      className={cn(
                        "grid size-9 shrink-0 place-items-center rounded-md font-mono text-xs tabular-nums",
                        trayCellClass(st, isNext),
                      )}
                    >
                      {st === "completed" ? (
                        <Check className="size-4" aria-hidden="true" />
                      ) : st === "coming_soon" ? (
                        <Lock className="size-3.5" aria-hidden="true" />
                      ) : (
                        <span>{l.order}</span>
                      )}
                    </div>
                  );

                  const body = (
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="font-bold text-foreground">
                          <Tx value={l.title} />
                        </span>
                        {l.kind === "project" && (
                          <Badge>
                            <FolderGit2 className="size-3.5" aria-hidden="true" /> {t("project")}
                          </Badge>
                        )}
                      </div>

                      {l.ready ? (
                        <div className="mt-0.5 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-foreground/80">
                          {l.duration && (
                            <span className="flex items-center gap-1 whitespace-nowrap">
                              <Clock className="size-3" aria-hidden="true" />
                              <span>{tc("minutes", { count: l.duration })}</span>
                            </span>
                          )}
                          <span className="flex items-center gap-1">
                            <BookOpen className="size-3" aria-hidden="true" />
                            <span>{ts(st)}</span>
                          </span>
                          {st === "locked" && missing.length > 0 && (
                            <span>
                              {t("prereqWarning", {
                                list: l.prerequisites
                                  .map((id) => loc.t(phase.lessons.find((x) => x.id === id)?.title) ?? id)
                                  .join(", "),
                              })}
                            </span>
                          )}
                        </div>
                      ) : (
                        l.outcomes && (
                          <div className="mt-0.5 truncate text-xs text-foreground/80">
                            {loc.t(l.outcomes).join(", ")}
                          </div>
                        )
                      )}
                    </div>
                  );

                  return (
                    <li key={l.id}>
                      {l.ready ? (
                        <Link
                          href={`/lesson/${l.id}/`}
                          data-lesson-row
                          data-live={isNext}
                          className={cn(
                            "group flex items-center gap-4 px-4 py-3 transition-colors hover:bg-accent hover:text-foreground focus-visible:outline-2 focus-visible:outline-ring focus-visible:-outline-offset-2",
                            isNext
                              ? "border-l-[3px] border-l-primary bg-accent"
                              : "border-l-[3px] border-l-transparent",
                          )}
                        >
                          {cell}
                          {body}
                          {parts && parts.fraction > 0 && st !== "completed" && (
                            <Progress value={parts.fraction} className="hidden w-24 sm:block" />
                          )}
                          <ArrowRight
                            aria-hidden="true"
                            className="size-4 shrink-0 transition-transform group-hover:translate-x-0.5 motion-reduce:transform-none"
                          />
                        </Link>
                      ) : (
                        <div className="flex items-center gap-4 border-l-[3px] border-l-transparent px-4 py-3 opacity-60">
                          {cell}
                          {body}
                        </div>
                      )}
                    </li>
                  );
                })}

                {prog.phaseTest && (
                  <li>
                    <Link
                      href={`/exam/${prog.phaseTest.id}/`}
                      className="group flex items-center gap-4 border-l-[3px] border-l-transparent px-4 py-3 transition-colors hover:bg-accent hover:text-foreground focus-visible:outline-2 focus-visible:outline-ring focus-visible:-outline-offset-2"
                    >
                      <div
                        className={cn(
                          "grid size-9 shrink-0 place-items-center rounded-md font-mono text-xs tabular-nums",
                          trayCellClass(prog.phaseTestPassed ? "completed" : "available", false),
                        )}
                      >
                        <ClipboardCheck className="size-4" aria-hidden="true" />
                      </div>
                      <div className="flex flex-1 flex-wrap items-baseline gap-x-2">
                        <span className="font-bold text-foreground">{t("phaseTest")}</span>
                        <span className="text-sm text-foreground/80">{loc.t(prog.phaseTest.title)}</span>
                      </div>
                      <ArrowRight
                        aria-hidden="true"
                        className="size-4 shrink-0 transition-transform group-hover:translate-x-0.5 motion-reduce:transform-none"
                      />
                    </Link>
                  </li>
                )}
              </ul>
            </li>
          );
        })}
      </ol>

      <div className="mt-10 grid gap-6 md:grid-cols-2">
        <Card className="p-5">
          <h3 className="mb-3 text-base font-bold text-foreground">{t("capstones")}</h3>
          <ul className="space-y-2 text-sm">
            {capstones.map((c) => {
              if (!c.ready) {
                return (
                  <li key={c.id} className="flex items-center gap-2 text-foreground/80">
                    <Lock className="size-3.5 shrink-0" aria-hidden="true" />
                    <span>
                      <Tx value={c.title} />
                    </span>
                  </li>
                );
              }
              const st = lessonStatus(p, c);
              const parts = lessonParts(p, c);
              const missing = c.prerequisites.filter((pre) => {
                const pl = findLesson(pre);
                return pl && pl.ready && !isLessonComplete(p, pl) && !p.skippedPhases.includes(pl.phaseId);
              });
              return (
                <li key={c.id}>
                  <Link
                    href={`/lesson/${c.id}/`}
                    data-lesson-row
                    className="group flex items-center gap-3 rounded-md border border-border px-3 py-2.5 transition-colors hover:bg-accent hover:text-foreground focus-visible:outline-2 focus-visible:outline-ring focus-visible:-outline-offset-2"
                  >
                    <div
                      className={cn(
                        "grid size-8 shrink-0 place-items-center rounded-md font-mono text-xs tabular-nums",
                        trayCellClass(st, false),
                      )}
                    >
                      {st === "completed" ? (
                        <Check className="size-4" aria-hidden="true" />
                      ) : (
                        <Trophy className="size-4" aria-hidden="true" />
                      )}
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="font-bold text-foreground">
                        <Tx value={c.title} />
                      </div>
                      <div className="mt-0.5 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-foreground/80">
                        {c.duration && (
                          <span className="flex items-center gap-1 whitespace-nowrap">
                            <Clock className="size-3" aria-hidden="true" />
                            <span>{tc("minutes", { count: c.duration })}</span>
                          </span>
                        )}
                        <span className="flex items-center gap-1">
                          <BookOpen className="size-3" aria-hidden="true" />
                          <span>{ts(st)}</span>
                        </span>
                        {st === "locked" && missing.length > 0 && (
                          <span>
                            {t("prereqWarning", {
                              list: missing.map((id) => loc.t(findLesson(id)?.title) ?? id).join(", "),
                            })}
                          </span>
                        )}
                      </div>
                    </div>
                    {parts.fraction > 0 && st !== "completed" && (
                      <Progress value={parts.fraction} className="hidden w-20 sm:block" />
                    )}
                    <ArrowRight
                      aria-hidden="true"
                      className="size-4 shrink-0 transition-transform group-hover:translate-x-0.5 motion-reduce:transform-none"
                    />
                  </Link>
                </li>
              );
            })}
          </ul>
        </Card>
        {catalog.furtherReading && (
          <Card className="p-5">
            <h3 className="mb-3 text-base font-bold text-foreground">{t("furtherReading")}</h3>
            <div className="flex flex-wrap gap-2">
              {loc.t(catalog.furtherReading).map((x) => (
                <Badge key={x} variant="outline">
                  {x}
                </Badge>
              ))}
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
