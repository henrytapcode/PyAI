"use client";

import { ArrowRight, CheckCircle2, Circle, Clock, Trophy } from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { useMemo } from "react";
import { XpFigure } from "@/components/count-up";
import { RoadmapTray } from "@/components/roadmap-tray";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { catalog, phaseOfLesson } from "@/lib/content";
import { Tx, useLoc } from "@/lib/i18n";
import { useProgress } from "@/lib/progress";
import {
  activityDays,
  dueKeys,
  isLessonComplete,
  lessonParts,
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
      <div className="flex flex-wrap items-end justify-between gap-4 animate-rise">
        <h1 className="text-2xl font-bold tracking-tight">
          {isNew ? t("greetingNew") : t("greeting")}
        </h1>

        <div className="grid w-full grid-cols-4 gap-2 sm:w-auto sm:flex sm:items-end sm:divide-x sm:divide-border sm:gap-0">
          <div className="text-left sm:pr-5">
            <div className="font-mono text-xl font-bold tabular-nums text-foreground sm:text-2xl">
              {data.days}
            </div>
            <div className="text-xs text-muted-foreground">{t("streak")}</div>
          </div>
          <div className="text-left sm:px-5">
            <div className="flex items-baseline gap-1 font-mono text-xl font-bold tabular-nums text-foreground sm:text-2xl">
              <span>{data.today}</span>
              <span className="font-mono text-xs tabular-nums text-muted-foreground">/{goal}</span>
            </div>
            <div className="text-xs text-muted-foreground">{t("xpToday")}</div>
          </div>
          <Link
            href="/review/"
            className="group relative block text-left outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring sm:px-5"
          >
            <div className="flex items-center gap-1 font-mono text-xl font-bold tabular-nums text-foreground sm:text-2xl">
              <span>{data.due}</span>
              {data.due > 0 && (
                <ArrowRight
                  className="size-3.5 text-foreground transition-transform duration-150 group-hover:translate-x-0.5 motion-reduce:transform-none"
                  aria-hidden="true"
                />
              )}
            </div>
            <div className="text-xs text-muted-foreground">{t("due")}</div>
          </Link>
          <div className="text-left sm:pl-5">
            <div className="font-mono text-xl font-bold tabular-nums text-foreground sm:text-2xl">
              <XpFigure value={p.xp} />
            </div>
            <div className="text-xs text-muted-foreground">{t("totalXp")}</div>
          </div>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Left column: next lesson + roadmap tray */}
        <div className="space-y-6 lg:col-span-2">
          {/* Next lesson card */}
          <Card className="animate-rise">
            <CardContent className="p-6">
              {data.next ? (
                <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
                  <div className="min-w-0 flex-1 space-y-2">
                    <div className="flex flex-wrap items-center gap-2">
                      <Badge variant="muted">{loc.t(data.nextPhase?.title)}</Badge>
                      <span className="text-xs font-bold text-primary-ink">
                        {isNew ? t("startTitle") : t("continueTitle")}
                      </span>
                    </div>
                    <h2 className="text-xl font-bold leading-tight tracking-tight">
                      <Tx value={data.next.title} />
                    </h2>
                    <p className="line-clamp-2 text-sm text-muted-foreground">
                      {loc.t(data.next.summary)}
                    </p>
                    <div className="flex items-center gap-3 pt-1">
                      <Progress value={lessonParts(p, data.next).fraction} className="max-w-xs" />
                      {data.next.duration && (
                        <span className="flex items-center gap-1 font-mono text-xs font-bold tabular-nums text-muted-foreground">
                          <Clock className="size-3.5" aria-hidden="true" />
                          {tc("minutes", { count: data.next.duration })}
                        </span>
                      )}
                    </div>
                  </div>
                  <Button asChild size="lg" className="shrink-0">
                    <Link href={`/lesson/${data.next.id}/`}>
                      {isNew ? tc("start") : tc("continue")}
                      <ArrowRight aria-hidden="true" />
                    </Link>
                  </Button>
                </div>
              ) : (
                <div className="flex items-center gap-4">
                  <Trophy className="size-10 text-primary" aria-hidden="true" />
                  <div>
                    <div className="font-bold">{t("allCaughtUp")}</div>
                    <Button asChild variant="link" className="px-0">
                      <Link href="/exams/">
                        {catalog.exams.length ? loc.t(catalog.exams[0].title) : ""}{" "}
                        <ArrowRight aria-hidden="true" />
                      </Link>
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Roadmap tray section */}
          <Card className="animate-rise">
            <CardHeader className="flex-row items-start justify-between gap-4">
              <div>
                <CardTitle>{t("skillTree")}</CardTitle>
                <CardDescription className="mt-1 flex flex-wrap gap-x-4">
                  <span>
                    {t("lessonsDone")}: {tc("of", { done: data.overall.lessonsDone, total: data.overall.lessonsReady })}
                  </span>
                  <span>
                    {t("exercisesPassed")}: {tc("of", { done: data.overall.exercisesPassed, total: data.overall.exercisesTotal })}
                  </span>
                </CardDescription>
              </div>
              <Button asChild variant="ghost" size="sm" className="shrink-0">
                <Link href="/learn/">
                  {t("openRoadmap")} <ArrowRight aria-hidden="true" />
                </Link>
              </Button>
            </CardHeader>
            <CardContent>
              <RoadmapTray variant="compact" nextId={data.next?.id} />
            </CardContent>
          </Card>
        </div>

        {/* Right column: weak topics + mastery */}
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
                        <span className="font-mono text-xs tabular-nums text-muted-foreground">
                          {t("accuracy", { rate: percent(w.rate) })}
                        </span>
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
              <Criterion
                done={(phase1?.exerciseRate ?? 0) >= 0.8}
                label={t("masteryExercises")}
                detail={percent(phase1?.exerciseRate ?? 0)}
              />
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
          <div className="overflow-x-auto pb-1">
            <div className="grid w-max grid-flow-col grid-rows-7 gap-1">
              {data.heat.map((d) => {
                const lvl = d.xp === 0 ? 0 : d.xp < goal / 3 ? 1 : d.xp < goal ? 2 : 3;
                return (
                  <div
                    key={d.key}
                    title={`${d.key}: ${d.xp} XP`}
                    className={cn(
                      "size-3.5 rounded-sm transition-opacity hover:opacity-80",
                      lvl === 0 && "bg-muted",
                      lvl === 1 && "bg-primary/35",
                      lvl === 2 && "bg-primary",
                      lvl === 3 && "bg-primary-ink",
                    )}
                  />
                );
              })}
            </div>
          </div>
          <div className="mt-3 flex items-center gap-1.5 text-xs font-bold text-muted-foreground">
            {t("less")}
            <span className="size-3 rounded-sm bg-muted" />
            <span className="size-3 rounded-sm bg-primary/35" />
            <span className="size-3 rounded-sm bg-primary" />
            <span className="size-3 rounded-sm bg-primary-ink" />
            {t("more")}
            <span className="ml-auto font-mono tabular-nums">{t("goal", { goal })}</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function Criterion({ done, label, detail }: { done: boolean; label: string; detail?: string }) {
  return (
    <div className="flex items-center gap-2.5">
      {done ? (
        <CheckCircle2 className="size-4 shrink-0 text-primary" aria-hidden="true" />
      ) : (
        <Circle className="size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
      )}
      <span className={cn("flex-1 font-bold", done && "text-muted-foreground line-through")}>
        {label}
      </span>
      {detail && (
        <span className="font-mono text-xs font-bold tabular-nums text-muted-foreground">
          {detail}
        </span>
      )}
    </div>
  );
}
