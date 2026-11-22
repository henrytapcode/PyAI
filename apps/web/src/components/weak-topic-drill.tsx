"use client";

import { ArrowRight, CheckCircle2, RotateCcw, Sparkles, Target, XCircle } from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { useEffect, useMemo, useState } from "react";
import { QuestionView } from "@/components/question";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { catalog, findLesson } from "@/lib/content";
import { useLoc } from "@/lib/i18n";
import { useProgress, XP, type AnswerRecord, type ProgressData } from "@/lib/progress";
import { emptyAnswer, grade as gradeAnswer, isAnswered, type UserAnswer } from "@/lib/quiz";
import { topicAccuracy, weakTopics } from "@/lib/selectors";
import type { Question } from "@/lib/types";
import { cn, percent, shuffle } from "@/lib/utils";

export interface WeakTopicDrillProps {
  questions: Question[];
  initialTopic?: string | null;
}

type DrillCount = 5 | 10 | 15;
type Phase = "setup" | "active" | "summary";

interface DrillResult {
  question: Question;
  correct: boolean;
}

const COUNTS: DrillCount[] = [5, 10, 15];

function prioritizeQuestions(pool: Question[], p: ProgressData): Question[] {
  const missed: Question[] = [];
  const unseen: Question[] = [];
  const seenOk: Question[] = [];
  for (const q of pool) {
    const stat = p.questionStats[q.id];
    if (!stat) {
      unseen.push(q);
    } else if (stat.wrong > stat.correct) {
      missed.push(q);
    } else {
      seenOk.push(q);
    }
  }
  missed.sort((a, b) => (p.questionStats[b.id]?.wrong ?? 0) - (p.questionStats[a.id]?.wrong ?? 0));
  return [...missed, ...shuffle(unseen), ...shuffle(seenOk)];
}

export function buildDrillQueue(
  questions: Question[],
  p: ProgressData,
  selectedTopic: string | "smart",
  count: DrillCount,
): Question[] {
  if (selectedTopic !== "smart") {
    const pool = questions.filter((q) => q.tags.includes(selectedTopic));
    return prioritizeQuestions(pool, p).slice(0, Math.min(count, pool.length));
  }

  const acc = topicAccuracy(p);
  const weakSet = new Set(acc.filter((t) => t.rate < 0.7).map((t) => t.topic));
  const rankedOrder = new Map(acc.map((t, idx) => [t.topic, idx]));

  const weakBucket: Question[] = [];
  const otherRanked: Question[] = [];
  const unseenTopics: Question[] = [];

  for (const q of questions) {
    const primary = q.tags[0];
    if (primary && weakSet.has(primary)) {
      weakBucket.push(q);
    } else if (primary && rankedOrder.has(primary)) {
      otherRanked.push(q);
    } else {
      unseenTopics.push(q);
    }
  }

  otherRanked.sort((a, b) => {
    const ra = rankedOrder.get(a.tags[0] ?? "") ?? 999;
    const rb = rankedOrder.get(b.tags[0] ?? "") ?? 999;
    return ra - rb;
  });

  const combined = [
    ...prioritizeQuestions(weakBucket, p),
    ...prioritizeQuestions(otherRanked, p),
    ...shuffle(unseenTopics),
  ];

  const seen = new Set<string>();
  const picked: Question[] = [];
  for (const q of combined) {
    if (seen.has(q.id)) continue;
    seen.add(q.id);
    picked.push(q);
    if (picked.length >= count) break;
  }
  return picked;
}

export function WeakTopicDrill({ questions, initialTopic }: WeakTopicDrillProps) {
  const t = useTranslations("review.drill");
  const tr = useTranslations("review");
  const tq = useTranslations("quiz");
  const tc = useTranslations("common");
  const loc = useLoc();

  const p = useProgress();
  const recordDrill = useProgress((s) => s.recordDrill);

  const availableTopics = useMemo(() => {
    const counts = new Map<string, number>();
    for (const q of questions) {
      for (const tag of q.tags) {
        counts.set(tag, (counts.get(tag) ?? 0) + 1);
      }
    }
    const accMap = new Map(topicAccuracy(p).map((a) => [a.topic, a.rate]));
    return Array.from(counts.entries())
      .map(([topic, count]) => ({ topic, count, rate: accMap.get(topic) }))
      .sort((a, b) => {
        if (a.rate !== undefined && b.rate !== undefined) return a.rate - b.rate;
        if (a.rate !== undefined) return -1;
        if (b.rate !== undefined) return 1;
        return b.count - a.count;
      });
  }, [questions, p]);

  const validInitialTopic = useMemo(() => {
    if (!initialTopic) return "smart" as const;
    return availableTopics.some((item) => item.topic === initialTopic) ? initialTopic : ("smart" as const);
  }, [initialTopic, availableTopics]);

  const [selectedTopic, setSelectedTopic] = useState<string | "smart">(validInitialTopic);
  const [count, setCount] = useState<DrillCount>(10);
  const [phase, setPhase] = useState<Phase>("setup");
  const [queue, setQueue] = useState<Question[]>([]);
  const [pos, setPos] = useState(0);
  const [answer, setAnswer] = useState<UserAnswer>({ type: "mcq", choice: null });
  const [revealed, setRevealed] = useState(false);
  const [results, setResults] = useState<DrillResult[]>([]);

  useEffect(() => {
    if (initialTopic && availableTopics.some((item) => item.topic === initialTopic)) {
      setSelectedTopic(initialTopic);
      setPhase("setup");
    }
  }, [initialTopic, availableTopics]);

  const accuracyList = useMemo(() => topicAccuracy(p), [p]);
  const weakList = useMemo(() => weakTopics(p), [p]);
  const overviewTopics = (weakList.length ? weakList : accuracyList).slice(0, 5);

  const matchingPoolSize = useMemo(() => {
    if (selectedTopic === "smart") return questions.length;
    return questions.filter((q) => q.tags.includes(selectedTopic)).length;
  }, [questions, selectedTopic]);

  const startSession = (topicOverride?: string | "smart") => {
    const targetTopic = topicOverride ?? selectedTopic;
    if (topicOverride !== undefined) setSelectedTopic(topicOverride);
    const nextQueue = buildDrillQueue(questions, p, targetTopic, count);
    if (nextQueue.length === 0) return;
    setQueue(nextQueue);
    setPos(0);
    setAnswer(emptyAnswer(nextQueue[0]));
    setRevealed(false);
    setResults([]);
    setPhase("active");
  };

  const commitAndFinish = (finalResults: DrillResult[]) => {
    if (finalResults.length > 0) {
      const records: AnswerRecord[] = finalResults.map((r) => ({
        questionId: r.question.id,
        correct: r.correct,
        tags: r.question.tags,
      }));
      recordDrill(records);
    }
    setPhase("summary");
  };

  const handleCheck = () => {
    const q = queue[pos];
    if (!q || revealed) return;
    const correct = gradeAnswer(q, answer);
    setRevealed(true);
    setResults((prev) => [...prev, { question: q, correct }]);
  };

  const handleNext = () => {
    const nextPos = pos + 1;
    if (nextPos >= queue.length) {
      commitAndFinish(results);
      return;
    }
    setPos(nextPos);
    setAnswer(emptyAnswer(queue[nextPos]));
    setRevealed(false);
  };

  const handleEndEarly = () => {
    commitAndFinish(results);
  };

  if (phase === "setup") {
    return (
      <div className="space-y-5 animate-rise">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <Target className="size-4 text-primary" aria-hidden="true" />
              {t("weakOverview")}
            </CardTitle>
            <CardDescription>{overviewTopics.length > 0 ? t("subtitle") : t("weakEmpty")}</CardDescription>
          </CardHeader>
          {overviewTopics.length > 0 && (
            <CardContent className="space-y-3">
              {overviewTopics.map((item) => {
                const isSelected = selectedTopic === item.topic;
                return (
                  <button
                    key={item.topic}
                    type="button"
                    onClick={() => setSelectedTopic(isSelected ? "smart" : item.topic)}
                    className={cn(
                      "block w-full rounded-md border p-3 text-left transition-colors outline-none focus-visible:outline-2 focus-visible:outline-ring",
                      isSelected ? "border-primary bg-accent/60" : "border-border bg-card hover:bg-accent/30",
                    )}
                  >
                    <div className="mb-1.5 flex items-center justify-between gap-2 text-sm font-bold">
                      <span>{loc.t(catalog.topics[item.topic]) ?? item.topic}</span>
                      <span className="font-mono text-xs tabular-nums text-muted-foreground">
                        {item.correct}/{item.total} ({percent(item.rate)})
                      </span>
                    </div>
                    <Progress value={item.rate} tone={item.rate >= 0.7 ? "success" : "primary"} />
                  </button>
                );
              })}
            </CardContent>
          )}
        </Card>

        <Card>
          <CardContent className="space-y-5 p-6">
            <div className="space-y-2">
              <div className="text-sm font-bold text-foreground">{t("chooseTopic")}</div>
              <div className="flex flex-wrap gap-1.5">
                <ChipButton active={selectedTopic === "smart"} onClick={() => setSelectedTopic("smart")}>
                  <Sparkles className="size-3.5" aria-hidden="true" />
                  {t("smartMix")}
                </ChipButton>
                {availableTopics.map((item) => (
                  <ChipButton
                    key={item.topic}
                    active={selectedTopic === item.topic}
                    onClick={() => setSelectedTopic(item.topic)}
                  >
                    {loc.t(catalog.topics[item.topic]) ?? item.topic}
                    {item.rate !== undefined ? ` · ${percent(item.rate)}` : ` · ${item.count}`}
                  </ChipButton>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <div className="text-sm font-bold text-foreground">{t("questionCount")}</div>
              <div className="flex flex-wrap gap-2">
                {COUNTS.map((n) => (
                  <ChipButton key={n} active={count === n} onClick={() => setCount(n)}>
                    {tc("questions", { count: n })}
                  </ChipButton>
                ))}
              </div>
            </div>

            <div className="flex flex-wrap items-center justify-between gap-3 border-t border-border pt-4">
              <span className="font-mono text-xs tabular-nums text-muted-foreground">
                {t("availableCount", { count: matchingPoolSize })}
              </span>
              <Button size="lg" type="button" disabled={matchingPoolSize === 0} onClick={() => startSession()}>
                {t("start")}
                <ArrowRight aria-hidden="true" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (phase === "active") {
    const q = queue[pos];
    if (!q) return null;
    const lesson = q.lessonId ? findLesson(q.lessonId) : undefined;
    const isLast = pos + 1 >= queue.length;

    return (
      <div className="space-y-4">
        <div className="flex items-center gap-3">
          <span className="font-mono text-sm font-medium tabular-nums text-foreground">
            {pos + 1}/{queue.length}
          </span>
          <Progress value={(pos + (revealed ? 1 : 0)) / queue.length} className="flex-1" />
          <Button type="button" variant="ghost" size="sm" onClick={handleEndEarly}>
            {t("quit")}
          </Button>
        </div>

        <Card className="animate-rise" key={`${q.id}-${pos}`}>
          <CardContent className="space-y-4 p-6 sm:p-8">
            <div className="flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
              {q.tags[0] && <Badge variant="muted">{loc.t(catalog.topics[q.tags[0]]) ?? q.tags[0]}</Badge>}
              {lesson && (
                <Link
                  href={`/lesson/${lesson.id}/`}
                  className="hit rounded-sm underline-offset-4 hover:text-foreground hover:underline focus-visible:outline-2 focus-visible:outline-ring"
                >
                  {tr("fromLesson", { lesson: loc.t(lesson.title) })}
                </Link>
              )}
            </div>
            <QuestionView question={q} answer={answer} onChange={setAnswer} revealed={revealed} showType={false} />
          </CardContent>
        </Card>

        {revealed ? (
          <Button size="lg" type="button" className="w-full" onClick={handleNext}>
            {isLast ? t("finish") : tc("next")}
            <ArrowRight aria-hidden="true" />
          </Button>
        ) : (
          <Button size="lg" type="button" className="w-full" disabled={!isAnswered(q, answer)} onClick={handleCheck}>
            {tq("check")}
          </Button>
        )}
      </div>
    );
  }

  // Summary phase
  const total = results.length;
  const correctCount = results.filter((r) => r.correct).length;
  const rate = total > 0 ? correctCount / total : 0;
  const xpEarned = correctCount * XP.review;

  const byTopic = new Map<string, { correct: number; total: number }>();
  for (const r of results) {
    const tag = r.question.tags[0] ?? "general";
    const entry = byTopic.get(tag) ?? { correct: 0, total: 0 };
    entry.total += 1;
    if (r.correct) entry.correct += 1;
    byTopic.set(tag, entry);
  }
  const topicRows = Array.from(byTopic.entries()).sort((a, b) => a[1].correct / a[1].total - b[1].correct / b[1].total);
  const missedResults = results.filter((r) => !r.correct);

  return (
    <div className="space-y-5 animate-rise">
      <Card>
        <CardContent className="flex flex-col items-center gap-3 p-6 text-center sm:p-8">
          <CheckCircle2 className="size-9 text-primary" aria-hidden="true" />
          <div>
            <h2 className="text-xl font-bold">{t("summaryTitle")}</h2>
            <p className="mt-1 font-mono text-sm tabular-nums text-muted-foreground">
              {t("scoreLabel", { correct: correctCount, total, rate: percent(rate) })}
            </p>
          </div>
          {xpEarned > 0 && <Badge variant="success">{t("xpEarned", { xp: xpEarned })}</Badge>}
          <div className="mt-2 flex flex-wrap justify-center gap-3">
            <Button type="button" onClick={() => startSession()}>
              <RotateCcw aria-hidden="true" />
              {t("drillAgain")}
            </Button>
            <Button type="button" variant="outline" onClick={() => setPhase("setup")}>
              {t("changeTopic")}
            </Button>
          </div>
        </CardContent>
      </Card>

      {topicRows.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">{t("topicBreakdown")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {topicRows.map(([topic, stat]) => {
              const r = stat.total ? stat.correct / stat.total : 0;
              return (
                <div key={topic}>
                  <div className="mb-1 flex justify-between text-sm font-bold">
                    <span>{loc.t(catalog.topics[topic]) ?? topic}</span>
                    <span className="font-mono text-xs tabular-nums text-muted-foreground">
                      {stat.correct}/{stat.total} ({percent(r)})
                    </span>
                  </div>
                  <Progress value={r} tone={r >= 0.7 ? "success" : "primary"} />
                </div>
              );
            })}
          </CardContent>
        </Card>
      )}

      {missedResults.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">{t("missedTitle")}</CardTitle>
            <CardDescription>{t("missedHint")}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2.5">
            {missedResults.map(({ question }) => {
              const lesson = question.lessonId ? findLesson(question.lessonId) : undefined;
              const prompt = loc.pick(question).value?.prompt ?? "";
              return (
                <div key={question.id} className="flex items-start justify-between gap-3 rounded-md border border-border p-3">
                  <div className="flex min-w-0 items-start gap-2">
                    <XCircle className="mt-0.5 size-4 shrink-0 text-danger" aria-hidden="true" />
                    <div className="min-w-0 text-sm">
                      <p className="line-clamp-2 font-medium text-foreground">{prompt}</p>
                      {lesson && (
                        <Link
                          href={`/lesson/${lesson.id}/`}
                          className="hit mt-1 inline-flex items-center gap-1 text-xs font-bold text-primary-ink underline-offset-4 hover:underline"
                        >
                          {t("openLesson")}: {loc.t(lesson.title)}
                        </Link>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function ChipButton({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      aria-pressed={active}
      onClick={onClick}
      className={cn(
        "hit inline-flex h-9 items-center gap-1.5 rounded-full border px-3 text-sm transition-colors outline-none focus-visible:outline-2 focus-visible:outline-ring",
        active
          ? "border-primary bg-accent font-bold text-primary"
          : "border-border bg-card text-foreground hover:bg-accent",
      )}
    >
      {children}
    </button>
  );
}
