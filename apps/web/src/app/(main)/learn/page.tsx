"use client";

import { ArrowRight, BookOpen, Check, ClipboardCheck, Clock, Cpu, FolderGit2, Lock, Trophy } from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { PageHeader } from "@/components/page-header";
import { PhaseIcon } from "@/components/phase-icon";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { catalog } from "@/lib/content";
import { Tx, useLoc } from "@/lib/i18n";
import { useProgress } from "@/lib/progress";
import { lessonParts, lessonStatus, phaseProgress, type LessonStatus } from "@/lib/selectors";
import { cn, percent } from "@/lib/utils";

const STATUS_DOT: Record<LessonStatus, string> = {
  completed: "bg-success border-success text-white",
  in_progress: "bg-accent border-primary text-primary",
  available: "bg-card border-primary/40 text-primary",
  locked: "bg-card border-border text-muted-foreground",
  skipped: "bg-muted border-border text-muted-foreground",
  coming_soon: "bg-card border-dashed border-border text-muted-foreground/50",
};

export default function LearnPage() {
  const t = useTranslations("learn");
  const tc = useTranslations("common");
  const ts = useTranslations("status");
  const loc = useLoc();
  const p = useProgress();
  const placement = catalog.exams.find((e) => e.kind === "placement");

  return (
    <div>
      <PageHeader title={t("title")} subtitle={t("subtitle")} />

      {p.profile.track === "B" && !p.placement && placement && (
        <Card className="mb-8 flex flex-wrap items-center gap-4 border-primary/30 bg-accent/40 p-5 animate-rise">
          <Trophy className="size-6 text-primary" />
          <p className="flex-1 text-sm">{t("trackB")}</p>
          <Button asChild size="sm">
            <Link href="/placement/">{t("takePlacement")}</Link>
          </Button>
        </Card>
      )}

      <ol className="relative space-y-6">
        {catalog.phases.map((phase) => {
          const prog = phaseProgress(p, phase);
          const hasContent = prog.ready > 0;
          return (
            <li key={phase.id} className="relative animate-rise">
              <Card className={cn("overflow-hidden", !hasContent && "bg-card/60")}>
                <div className="flex flex-wrap items-center gap-4 border-b p-5">
                  <div
                    className={cn(
                      "grid size-12 place-items-center rounded-2xl",
                      hasContent ? "bg-primary text-primary-foreground shadow-md shadow-primary/20" : "bg-muted text-muted-foreground",
                    )}
                  >
                    <PhaseIcon name={phase.icon} className="size-6" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="text-xs font-medium uppercase tracking-wide text-muted-foreground">{t("phase", { n: phase.order })}</div>
                    <h2 className="text-lg font-semibold">
                      <Tx value={phase.title} />
                    </h2>
                    <p className="text-sm text-muted-foreground">{loc.t(phase.summary)}</p>
                  </div>
                  <div className="flex flex-col items-end gap-1.5">
                    <div className="flex flex-wrap justify-end gap-1.5">
                      {phase.runner === "local" && (
                        <Badge variant="outline">
                          <Cpu /> {t("localRunner")}
                        </Badge>
                      )}
                      {prog.skipped && <Badge variant="muted">{ts("skipped")}</Badge>}
                      {!hasContent && <Badge variant="outline">{tc("comingSoon")}</Badge>}
                    </div>
                    {hasContent && (
                      <div className="flex w-40 items-center gap-2">
                        <Progress value={prog.fraction} />
                        <span className="text-xs tabular-nums text-muted-foreground">{percent(prog.fraction)}</span>
                      </div>
                    )}
                  </div>
                </div>

                <ul className="divide-y">
                  {phase.lessons.map((l) => {
                    const st = lessonStatus(p, { ...l, phaseId: phase.id });
                    const parts = l.ready ? lessonParts(p, l) : null;
                    const missing = l.prerequisites.filter((pre) => !phase.lessons.some((x) => x.id === pre) || st === "locked");
                    const content = (
                      <div className="flex items-center gap-4 px-5 py-3.5">
                        <span className={cn("grid size-8 shrink-0 place-items-center rounded-full border-2 text-xs font-semibold", STATUS_DOT[st])}>
                          {st === "completed" ? <Check className="size-4" /> : st === "coming_soon" ? <Lock className="size-3.5" /> : l.order}
                        </span>
                        <div className="min-w-0 flex-1">
                          <div className="flex flex-wrap items-center gap-2">
                            <span className={cn("font-medium", !l.ready && "text-muted-foreground")}>
                              <Tx value={l.title} />
                            </span>
                            {l.kind === "project" && (
                              <Badge>
                                <FolderGit2 /> {t("project")}
                              </Badge>
                            )}
                          </div>
                          {l.ready ? (
                            <div className="mt-0.5 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-muted-foreground">
                              {l.duration && (
                                <span className="flex items-center gap-1">
                                  <Clock className="size-3" />
                                  {tc("minutes", { count: l.duration })}
                                </span>
                              )}
                              <span className="flex items-center gap-1">
                                <BookOpen className="size-3" />
                                {ts(st)}
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
                            l.outcomes && <div className="mt-0.5 truncate text-xs text-muted-foreground">{loc.t(l.outcomes).join(" · ")}</div>
                          )}
                        </div>
                        {parts && parts.fraction > 0 && st !== "completed" && <Progress value={parts.fraction} className="hidden w-24 sm:block" />}
                        {l.ready && <ArrowRight className="size-4 text-muted-foreground transition group-hover:translate-x-0.5 group-hover:text-foreground" />}
                      </div>
                    );
                    return (
                      <li key={l.id}>
                        {l.ready ? (
                          <Link href={`/lesson/${l.id}/`} className="group block transition hover:bg-muted/50">
                            {content}
                          </Link>
                        ) : (
                          <div className="cursor-default opacity-80">{content}</div>
                        )}
                      </li>
                    );
                  })}
                  {prog.phaseTest && (
                    <li>
                      <Link href={`/exam/${prog.phaseTest.id}/`} className="group flex items-center gap-4 bg-muted/30 px-5 py-3.5 transition hover:bg-muted/60">
                        <span className={cn("grid size-8 place-items-center rounded-full", prog.phaseTestPassed ? "bg-success text-white" : "bg-primary/10 text-primary")}>
                          <ClipboardCheck className="size-4" />
                        </span>
                        <span className="flex-1 font-medium">
                          {t("phaseTest")} · {loc.t(prog.phaseTest.title)}
                        </span>
                        <ArrowRight className="size-4 text-muted-foreground" />
                      </Link>
                    </li>
                  )}
                </ul>
              </Card>
            </li>
          );
        })}
      </ol>

      <div className="mt-10 grid gap-6 md:grid-cols-2">
        <Card className="p-5">
          <h3 className="mb-3 font-semibold">{t("capstones")}</h3>
          <ul className="space-y-2 text-sm">
            {catalog.capstones.map((c) => (
              <li key={c.id} className="flex items-center gap-2 text-muted-foreground">
                <Lock className="size-3.5" />
                <Tx value={c.title} />
              </li>
            ))}
          </ul>
        </Card>
        {catalog.furtherReading && (
          <Card className="p-5">
            <h3 className="mb-3 font-semibold">{t("furtherReading")}</h3>
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
