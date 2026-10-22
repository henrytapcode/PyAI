"use client";

import { ArrowRight, Check, CheckCircle2, Circle, Clock, Flame, Repeat, Sparkles, Target, Trophy } from "lucide-react";
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
        <p className="text-sm text-muted-foreground">{isNew ? t("greetingNew") : t("greeting")}</p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">PyAI Path</h1>
      </div>

      {/* Continue */}
      <Card className="relative overflow-hidden animate-rise">
        <div className="pointer-events-none absolute -right-16 -top-16 size-56 rounded-full bg-primary/10 blur-2xl" />
        <CardContent className="flex flex-col gap-5 p-6 sm:flex-row sm:items-center">
          {data.next ? (
            <>
              <div className="grid size-14 shrink-0 place-items-center rounded-2xl bg-primary text-primary-foreground shadow-lg shadow-primary/25">
                <PhaseIcon name={data.nextPhase?.icon ?? "code"} className="size-7" />
              </div>
              <div className="min-w-0 flex-1">
                <div className="text-xs font-medium uppercase tracking-wide text-primary">
                  {isNew ? t("startTitle") : t("continueTitle")} · {loc.t(data.nextPhase?.title)}
                </div>
                <div className="mt-1 text-xl font-semibold">
                  <Tx value={data.next.title} />
                </div>
                <div className="mt-1 line-clamp-2 text-sm text-muted-foreground">{loc.t(data.next.summary)}</div>
                <div className="mt-3 flex items-center gap-3">
                  <Progress value={lessonParts(p, data.next).fraction} className="max-w-xs" />
                  {data.next.duration && (
                    <span className="flex items-center gap-1 text-xs text-muted-foreground">
                      <Clock className="size-3.5" />
                      {tc("minutes", { count: data.next.duration })}
                    </span>
                  )}
                </div>
              </div>
              <Button asChild size="lg" className="shrink-0">
                <Link href={`/lesson/${data.next.id}/`}>
                  {isNew ? tc("start") : tc("continue")}
                  <ArrowRight />
                </Link>
              </Button>
            </>
          ) : (
            <div className="flex items-center gap-4">
              <Trophy className="size-10 text-warning" />
              <div>
                <div className="font-semibold">{t("allCaughtUp")}</div>
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

      {/* Stats */}
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <StatCard icon={<Flame className={cn("size-5", data.days ? "text-warning" : "text-muted-foreground")} />} label={t("streak")} value={data.days} />
        <Card className="animate-rise">
          <CardContent className="flex items-center gap-3 p-4">
            <Ring value={data.today / goal} size={48} stroke={5}>
              <Target className="size-4 text-primary" />
            </Ring>
            <div>
              <div className="text-xl font-semibold leading-none">
                {data.today}
                <span className="text-sm font-normal text-muted-foreground">/{goal}</span>
              </div>
              <div className="mt-1 text-xs text-muted-foreground">{t("xpToday")}</div>
            </div>
          </CardContent>
        </Card>
        <Link href="/review/" className="group">
          <StatCard
            icon={<Repeat className="size-5 text-primary" />}
            label={t("due")}
            value={data.due}
            extra={data.due > 0 ? <ArrowRight className="size-4 text-primary transition group-hover:translate-x-0.5" /> : null}
          />
        </Link>
        <StatCard icon={<Sparkles className="size-5 text-primary" />} label={t("totalXp")} value={p.xp} />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Skill tree */}
        <Card className="lg:col-span-2 animate-rise">
          <CardHeader className="flex-row items-center justify-between">
            <div>
              <CardTitle>{t("skillTree")}</CardTitle>
              <CardDescription>
                {t("lessonsDone")}: {tc("of", { done: data.overall.lessonsDone, total: data.overall.lessonsReady })} · {t("exercisesPassed")}:{" "}
                {tc("of", { done: data.overall.exercisesPassed, total: data.overall.exercisesTotal })}
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
                <div key={ph.id} className={cn("rounded-xl px-3 py-2.5", active && "bg-accent/50")}>
                  <div className="flex items-center gap-3">
                    <Ring value={prog.skipped ? 1 : prog.fraction} size={40} stroke={4}>
                      <PhaseIcon name={ph.icon} className={cn("size-4", prog.ready ? "text-foreground" : "text-muted-foreground")} />
                    </Ring>
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-muted-foreground">{ph.order}</span>
                        <span className={cn("truncate text-sm font-medium", !prog.ready && "text-muted-foreground")}>{loc.t(ph.title)}</span>
                        {prog.skipped && <Badge variant="muted">{ts("skipped")}</Badge>}
                        {!prog.ready && <Badge variant="outline">{tc("comingSoon")}</Badge>}
                      </div>
                      {active && (
                        <div className="mt-2 flex flex-wrap gap-1.5">
                          {ph.lessons.map((l) => {
                            const st = lessonStatus(p, { ...l, phaseId: ph.id });
                            return (
                              <Link
                                key={l.id}
                                href={l.ready ? `/lesson/${l.id}/` : "/learn/"}
                                title={`${loc.t(l.title)} · ${ts(st)}`}
                                className={cn(
                                  "grid size-7 place-items-center rounded-lg border text-[11px] font-semibold transition hover:scale-105",
                                  st === "completed" && "border-success bg-success text-white",
                                  st === "in_progress" && "border-primary bg-accent text-accent-foreground",
                                  (st === "available" || st === "locked") && "bg-card",
                                  st === "skipped" && "bg-muted text-muted-foreground",
                                  st === "coming_soon" && "border-dashed text-muted-foreground/60",
                                )}
                              >
                                {st === "completed" ? <Check className="size-3.5" /> : l.order}
                              </Link>
                            );
                          })}
                        </div>
                      )}
                    </div>
                    <span className="text-xs tabular-nums text-muted-foreground">{prog.ready ? percent(prog.skipped ? 1 : prog.fraction) : ""}</span>
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
                      <div className="mb-1 flex justify-between text-sm">
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

      {/* Activity heatmap */}
      <Card className="animate-rise">
        <CardHeader>
          <CardTitle>{t("activity")}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <div className="grid w-max grid-flow-col grid-rows-7 gap-1">
              {data.heat.map((d) => {
                const lvl = d.xp === 0 ? 0 : d.xp < goal / 3 ? 1 : d.xp < goal ? 2 : 3;
                return (
                  <div
                    key={d.key}
                    title={`${d.key}: ${d.xp} XP`}
                    className={cn(
                      "size-3.5 rounded-[4px]",
                      lvl === 0 && "bg-muted",
                      lvl === 1 && "bg-primary/30",
                      lvl === 2 && "bg-primary/60",
                      lvl === 3 && "bg-primary",
                    )}
                  />
                );
              })}
            </div>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-xs text-muted-foreground">
            {t("less")}
            <span className="size-3 rounded-[3px] bg-muted" />
            <span className="size-3 rounded-[3px] bg-primary/30" />
            <span className="size-3 rounded-[3px] bg-primary/60" />
            <span className="size-3 rounded-[3px] bg-primary" />
            {t("more")}
            <span className="ml-auto">{t("goal", { goal })}</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function StatCard({ icon, label, value, extra }: { icon: React.ReactNode; label: string; value: React.ReactNode; extra?: React.ReactNode }) {
  return (
    <Card className="h-full animate-rise transition hover:shadow-md">
      <CardContent className="flex items-center gap-3 p-4">
        <div className="grid size-12 place-items-center rounded-xl bg-muted">{icon}</div>
        <div className="min-w-0 flex-1">
          <div className="text-xl font-semibold leading-none tabular-nums">{value}</div>
          <div className="mt-1 truncate text-xs text-muted-foreground">{label}</div>
        </div>
        {extra}
      </CardContent>
    </Card>
  );
}

function Criterion({ done, label, detail }: { done: boolean; label: string; detail?: string }) {
  return (
    <div className="flex items-center gap-2.5">
      {done ? <CheckCircle2 className="size-4 text-success" /> : <Circle className="size-4 text-muted-foreground" />}
      <span className={cn("flex-1", done && "text-muted-foreground line-through decoration-success/50")}>{label}</span>
      {detail && <span className="text-xs tabular-nums text-muted-foreground">{detail}</span>}
    </div>
  );
}
