"use client";

import { ArrowRight, Check, CheckCircle2, Circle, Clock, Trophy } from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { useMemo } from "react";
import { PhaseIcon } from "@/components/phase-icon";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress, Ring } from "@/components/ui/progress";
import { catalog, phaseOfLesson } from "@/lib/content";
import { Tx, useLoc } from "@/lib/i18n";
import { useProgress } from "@/lib/progress";
import {
  activityDays,
  dueKeys,
  isLessonComplete,
  lessonParts,
  lessonStatus,
  nextLesson,
  overallProgress,
  phaseProgress,
  streak,
  topicAccuracy,
  weakTopics,
} from "@/lib/selectors";
import { cn, percent, todayKey } from "@/lib/utils";

export default function DashboardPage() {
  const t = useTranslations("dashboard");
  const tc = useTranslations("common");
  const ts = useTranslations("status");
  const loc = useLoc();
  const p = useProgress();

  const data = useMemo(() => {
    const next = nextLesson(p);
    return {
      next,
      nextPhase: next ? phaseOfLesson(next.id) : undefined,
      days: streak(p),
      today: p.activity[todayKey()] ?? 0,
      due: dueKeys(p).length,
      overall: overallProgress(p),
      weak: weakTopics(p),
      accuracy: topicAccuracy(p),
      heat: activityDays(p),
      phases: catalog.phases.map((ph) => ({ ph, prog: phaseProgress(p, ph) })),
    };
  }, [p]);

  const isNew = data.overall.lessonsDone === 0 && Object.keys(p.lessons).length === 0;
  const goal = p.profile.dailyGoal;
  const mockPassed = Object.entries(p.exams).some(([id, a]) => id.startsWith("mock") && a.some((x) => x.score >= 0.8));
  const projectsDone = catalog.phases
    .flatMap((ph) => ph.lessons)
    .filter((l) => l.kind === "project" && l.ready && isLessonComplete(p, l)).length;
  const phase1 = data.phases.find((x) => x.ph.id === "p1")?.prog;

  return (
    <div className="space-y-6">
      <div className="animate-rise">
        <p className="text-sm font-bold text-muted-foreground">{isNew ? t("greetingNew") : t("greeting")}</p>
        <h1 className="display mt-2 text-4xl sm:text-5xl">PyAI Path</h1>
      </div>

      {/* Continue: the cabinet's start screen */}
      <Card className="crt animate-rise">
        <CardContent className="flex flex-col gap-5 p-6 sm:flex-row sm:items-center">
          {data.next ? (
            <>
              <div className="grid size-14 shrink-0 place-items-center rounded-[4px] border-2 border-edge bg-primary text-primary-foreground shadow-[4px_4px_0_var(--hit)]">
                <PhaseIcon name={data.nextPhase?.icon ?? "code"} className="size-7" />
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-baseline gap-x-3 text-sm font-bold">
                  <span className="text-primary-ink">{isNew ? t("startTitle") : t("continueTitle")}</span>
                  <span className="text-muted-foreground">{loc.t(data.nextPhase?.title)}</span>
                </div>
                <div className="mt-1 text-2xl font-black leading-tight tracking-tight">
                  <Tx value={data.next.title} />
                </div>
                <div className="mt-1 line-clamp-2 text-sm text-muted-foreground">{loc.t(data.next.summary)}</div>
                <div className="mt-3 flex items-center gap-3">
                  <Progress value={lessonParts(p, data.next).fraction} className="max-w-xs" />
                  {data.next.duration && (
                    <span className="flex items-center gap-1 text-xs font-bold text-muted-foreground">
                      <Clock className="size-3.5" />
                      {tc("minutes", { count: data.next.duration })}
                    </span>
                  )}
                </div>
              </div>
              <Button asChild size="lg" className="relative z-10 shrink-0">
                <Link href={`/lesson/${data.next.id}/`}>
                  {isNew ? tc("start") : tc("continue")}
                  <ArrowRight />
                </Link>
              </Button>
            </>
          ) : (
            <div className="flex items-center gap-4">
              <Trophy className="size-10 text-hit" />
              <div>
                <div className="font-black">{t("allCaughtUp")}</div>
                <Button asChild variant="link" className="px-0">
                  <Link href="/exams/">
                    {catalog.exams.length ? loc.t(catalog.exams[0].title) : ""} <ArrowRight />
                  </Link>
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Score line: figures parted by bar rules, ember and acid taking turns */}
      <Card className="crt animate-rise">
        <div className="grid grid-cols-2 lg:grid-cols-4 [&>*]:px-5 [&>*]:py-5 [&>*:nth-child(even)]:border-l-2 lg:[&>*:nth-child(n+2)]:border-l-2 max-lg:[&>*:nth-child(n+3)]:border-t-2">
          <ScoreCell label={t("streak")} value={data.days} tone="ember" />
          <ScoreCell label={t("xpToday")} value={data.today} tone="acid" suffix={`/${goal}`} />
          <Link href="/review/" className="group relative block">
            <ScoreCell label={t("due")} value={data.due} tone="ember" arrow={data.due > 0} />
          </Link>
          <ScoreCell label={t("totalXp")} value={p.xp} tone="acid" />
        </div>
      </Card>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Level select */}
        <Card className="animate-rise lg:col-span-2">
          <CardHeader className="flex-row items-center justify-between">
            <div>
              <CardTitle>{t("skillTree")}</CardTitle>
              <CardDescription className="flex flex-wrap gap-x-4">
                <span>
                  {t("lessonsDone")}: {tc("of", { done: data.overall.lessonsDone, total: data.overall.lessonsReady })}
                </span>
                <span>
                  {t("exercisesPassed")}: {tc("of", { done: data.overall.exercisesPassed, total: data.overall.exercisesTotal })}
                </span>
              </CardDescription>
            </div>
            <Button asChild variant="ghost" size="sm">
              <Link href="/learn/">
                {t("openRoadmap")} <ArrowRight />
              </Link>
            </Button>
          </CardHeader>
          <CardContent className="space-y-1">
            {data.phases.map(({ ph, prog }) => {
              const active = ph.id === data.nextPhase?.id;
              return (
                <div key={ph.id} data-live={active} className="row-cursor rounded-[4px] px-3 py-2.5">
                  <div className="flex items-center gap-3">
                    <Ring value={prog.skipped ? 1 : prog.fraction} size={40} stroke={4}>
                      <PhaseIcon name={ph.icon} className={cn("size-4", !prog.ready && "opacity-60")} />
                    </Ring>
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold opacity-70">{ph.order}</span>
                        <span className={cn("truncate text-sm font-bold", !prog.ready && "opacity-60")}>{loc.t(ph.title)}</span>
                        {prog.skipped && <Badge variant="muted">{ts("skipped")}</Badge>}
                        {!prog.ready && <Badge variant="outline" className={cn(active && "border-current text-current")}>{tc("comingSoon")}</Badge>}
                      </div>
                      {active && (
                        <div className="mt-2 flex flex-wrap gap-1.5">
                          {ph.lessons.map((l) => {
                            const st = lessonStatus(p, { ...l, phaseId: ph.id });
                            return (
                              <Link
                                key={l.id}
                                href={l.ready ? `/lesson/${l.id}/` : "/learn/"}
                                title={`${loc.t(l.title)}: ${ts(st)}`}
                                className={cn(
                                  "grid size-8 place-items-center rounded-[2px] border-2 text-[12px] font-bold text-foreground transition-transform hover:-translate-y-0.5 active:translate-y-0.5",
                                  st === "completed" && "border-success bg-success text-success-foreground",
                                  st === "in_progress" && "border-edge bg-accent text-accent-foreground",
                                  (st === "available" || st === "locked") && "border-edge bg-card",
                                  st === "skipped" && "border-border bg-muted text-muted-foreground",
                                  st === "coming_soon" && "border-dashed border-border bg-card text-muted-foreground",
                                )}
                              >
                                {st === "completed" ? <Check className="size-3.5" /> : l.order}
                              </Link>
                            );
                          })}
                        </div>
                      )}
                    </div>
                    <span className="text-xs font-bold tabular-nums opacity-70">{prog.ready ? percent(prog.skipped ? 1 : prog.fraction) : ""}</span>
                  </div>
                </div>
              );
            })}
          </CardContent>
        </Card>

        <div className="space-y-6">
          {/* Weak topics */}
          <Card className="animate-rise">
            <CardHeader>
              <CardTitle>{t("weakTopics")}</CardTitle>
            </CardHeader>
            <CardContent>
              {data.accuracy.length === 0 ? (
                <p className="text-sm text-muted-foreground">{t("weakTopicsEmpty")}</p>
              ) : (
                <div className="space-y-3">
                  {(data.weak.length ? data.weak : data.accuracy.slice(0, 4)).slice(0, 5).map((w) => (
                    <div key={w.topic}>
                      <div className="mb-1 flex justify-between text-sm font-bold">
                        <span>{loc.t(catalog.topics[w.topic]) ?? w.topic}</span>
                        <span className="text-xs text-muted-foreground">{t("accuracy", { rate: percent(w.rate) })}</span>
                      </div>
                      <Progress value={w.rate} tone={w.rate >= 0.7 ? "success" : "primary"} />
                    </div>
                  ))}
                  {data.due > 0 && (
                    <Button asChild variant="soft" size="sm" className="mt-1 w-full">
                      <Link href="/review/">{t("reviewNow")}</Link>
                    </Button>
                  )}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Mastery */}
          <Card className="animate-rise">
            <CardHeader>
              <CardTitle>{t("mastery")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2.5 text-sm">
              <Criterion done={(phase1?.exerciseRate ?? 0) >= 0.8} label={t("masteryExercises")} detail={percent(phase1?.exerciseRate ?? 0)} />
              <Criterion done={!!phase1?.phaseTestPassed} label={t("masteryPhaseTest")} />
              <Criterion done={projectsDone >= 4} label={t("masteryProjects")} detail={`${projectsDone}/4`} />
              <Criterion done={mockPassed} label={t("masteryMock")} />
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Activity heatmap: ember while building up, acid once the daily goal is hit */}
      <Card className="animate-rise">
        <CardHeader>
          <CardTitle>{t("activity")}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto pb-1">
            <div className="grid w-max grid-flow-col grid-rows-7 gap-1">
              {data.heat.map((d) => {
                const lvl = d.xp === 0 ? 0 : d.xp < goal / 3 ? 1 : d.xp < goal ? 2 : 3;
                return (
                  <div
                    key={d.key}
                    title={`${d.key}: ${d.xp} XP`}
                    className={cn(
                      "size-3.5 rounded-[2px] transition-transform hover:scale-150",
                      lvl === 0 && "bg-muted",
                      lvl === 1 && "bg-primary/35",
                      lvl === 2 && "bg-primary",
                      lvl === 3 && "bg-hit",
                    )}
                  />
                );
              })}
            </div>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-xs font-bold text-muted-foreground">
            {t("less")}
            <span className="size-3 rounded-[2px] bg-muted" />
            <span className="size-3 rounded-[2px] bg-primary/35" />
            <span className="size-3 rounded-[2px] bg-primary" />
            <span className="size-3 rounded-[2px] bg-hit" />
            {t("more")}
            <span className="ml-auto">{t("goal", { goal })}</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function ScoreCell({ label, value, tone, suffix, arrow }: { label: string; value: React.ReactNode; tone: "ember" | "acid"; suffix?: string; arrow?: boolean }) {
  return (
    <div className="relative z-10 transition-transform group-hover:-translate-y-0.5">
      <div className="flex items-baseline gap-1">
        <span className={cn("figure text-[44px] sm:text-[52px]", tone === "ember" ? "text-primary" : "text-hit")}>{value}</span>
        {suffix && <span className="text-sm font-bold text-muted-foreground">{suffix}</span>}
        {arrow && <ArrowRight className="ml-1 size-4 self-center text-foreground transition-transform group-hover:translate-x-1" />}
      </div>
      <div className="mt-2 truncate text-sm font-bold text-muted-foreground">{label}</div>
    </div>
  );
}

function Criterion({ done, label, detail }: { done: boolean; label: string; detail?: string }) {
  return (
    <div className="flex items-center gap-2.5">
      {done ? <CheckCircle2 className="size-4 text-success" /> : <Circle className="size-4 text-muted-foreground" />}
      <span className={cn("flex-1 font-bold", done && "text-muted-foreground line-through decoration-success decoration-2")}>{label}</span>
      {detail && <span className="text-xs font-bold tabular-nums text-muted-foreground">{detail}</span>}
    </div>
  );
}
