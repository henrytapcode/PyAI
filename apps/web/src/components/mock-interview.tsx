"use client";

import {
  AlertCircle,
  ArrowRight,
  CheckCircle2,
  Clock,
  Lightbulb,
  Pause,
  Play,
  RotateCcw,
  Sparkles,
} from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useMemo, useState } from "react";
import { Markdown, StaticCode } from "@/components/markdown";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { catalog } from "@/lib/content";
import { UntranslatedBadge, useLoc } from "@/lib/i18n";
import { useProgress } from "@/lib/progress";
import type { InterviewKind, InterviewQuestion } from "@/lib/types";
import { cn, formatDuration, shuffle } from "@/lib/utils";

export interface MockInterviewProps {
  questions: InterviewQuestion[];
}

type MockCount = 3 | 5 | 8;
type TimerOption = 0 | 120 | 300;
type SelfRating = "needs_work" | "partial" | "confident";
type Phase = "setup" | "active" | "summary";

interface MockResult {
  question: InterviewQuestion;
  rating: SelfRating;
  notes: string;
}

const COUNTS: MockCount[] = [3, 5, 8];
const TIMERS: TimerOption[] = [0, 120, 300];
const KINDS: InterviewKind[] = ["concept", "coding", "scenario", "system"];

export function MockInterview({ questions }: MockInterviewProps) {
  const t = useTranslations("interview.mock");
  const ti = useTranslations("interview");
  const tc = useTranslations("common");
  const loc = useLoc();

  const practiced = useProgress((s) => s.practiced);
  const setPracticed = useProgress((s) => s.setPracticed);

  const topics = useMemo(() => Array.from(new Set(questions.map((q) => q.topic))), [questions]);

  const [topic, setTopic] = useState<string>("all");
  const [level, setLevel] = useState<"all" | "junior" | "mid">("all");
  const [kind, setKind] = useState<"all" | InterviewKind>("all");
  const [count, setCount] = useState<MockCount>(5);
  const [timerSec, setTimerSec] = useState<TimerOption>(120);

  const [phase, setPhase] = useState<Phase>("setup");
  const [queue, setQueue] = useState<InterviewQuestion[]>([]);
  const [pos, setPos] = useState(0);
  const [notes, setNotes] = useState("");
  const [tipOpen, setTipOpen] = useState(false);
  const [revealed, setRevealed] = useState(false);
  const [remainingSec, setRemainingSec] = useState(0);
  const [paused, setPaused] = useState(false);
  const [elapsedSec, setElapsedSec] = useState(0);
  const [results, setResults] = useState<MockResult[]>([]);

  const matchingPool = useMemo(() => {
    return questions.filter((q) => {
      if (topic !== "all" && q.topic !== topic) return false;
      if (level !== "all" && q.level !== level) return false;
      if (kind !== "all" && q.kind !== kind) return false;
      return true;
    });
  }, [questions, topic, level, kind]);

  useEffect(() => {
    if (phase !== "active" || paused) return;
    const id = window.setInterval(() => {
      setElapsedSec((e) => e + 1);
      if (timerSec > 0) {
        setRemainingSec((r) => (r > 0 ? r - 1 : 0));
      }
    }, 1000);
    return () => window.clearInterval(id);
  }, [phase, paused, timerSec]);

  const beginQueue = (picked: InterviewQuestion[]) => {
    if (picked.length === 0) return;
    setQueue(picked);
    setPos(0);
    setNotes("");
    setTipOpen(false);
    setRevealed(false);
    setRemainingSec(timerSec);
    setPaused(false);
    setElapsedSec(0);
    setResults([]);
    setPhase("active");
  };

  const startSession = () => {
    const unpracticed = shuffle(matchingPool.filter((q) => !practiced?.[q.id]));
    const alreadyPracticed = shuffle(matchingPool.filter((q) => practiced?.[q.id]));
    const picked = [...unpracticed, ...alreadyPracticed].slice(0, Math.min(count, matchingPool.length));
    beginQueue(picked);
  };

  const handleRate = (rating: SelfRating) => {
    const q = queue[pos];
    if (!q) return;
    if (rating === "confident") {
      setPracticed(q.id, true);
    }
    const nextResults = [...results, { question: q, rating, notes: notes.trim() }];
    setResults(nextResults);

    const nextPos = pos + 1;
    if (nextPos >= queue.length) {
      setPhase("summary");
      return;
    }
    setPos(nextPos);
    setNotes("");
    setTipOpen(false);
    setRevealed(false);
    setRemainingSec(timerSec);
    setPaused(false);
  };

  const retryNeedsWork = () => {
    const missed = results.filter((r) => r.rating === "needs_work").map((r) => r.question);
    beginQueue(shuffle(missed));
  };

  if (phase === "setup") {
    return (
      <Card className="animate-rise">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Sparkles className="size-4 text-primary" aria-hidden="true" />
            {t("title")}
          </CardTitle>
          <CardDescription>{t("subtitle")}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-5">
          <div className="space-y-2">
            <div className="text-sm font-bold">{t("filterTopic")}</div>
            <div className="flex flex-wrap gap-1.5">
              <ChipButton active={topic === "all"} onClick={() => setTopic("all")}>
                {tc("all")}
              </ChipButton>
              {topics.map((tp) => (
                <ChipButton key={tp} active={topic === tp} onClick={() => setTopic(tp)}>
                  {loc.t(catalog.topics[tp]) ?? tp}
                </ChipButton>
              ))}
            </div>
          </div>

          <div className="grid gap-5 sm:grid-cols-2">
            <div className="space-y-2">
              <div className="text-sm font-bold">{t("filterLevel")}</div>
              <div className="flex flex-wrap gap-1.5">
                <ChipButton active={level === "all"} onClick={() => setLevel("all")}>
                  {tc("all")}
                </ChipButton>
                <ChipButton active={level === "junior"} onClick={() => setLevel("junior")}>
                  {ti("level.junior")}
                </ChipButton>
                <ChipButton active={level === "mid"} onClick={() => setLevel("mid")}>
                  {ti("level.mid")}
                </ChipButton>
              </div>
            </div>

            <div className="space-y-2">
              <div className="text-sm font-bold">{t("filterKind")}</div>
              <div className="flex flex-wrap gap-1.5">
                <ChipButton active={kind === "all"} onClick={() => setKind("all")}>
                  {tc("all")}
                </ChipButton>
                {KINDS.map((k) => (
                  <ChipButton key={k} active={kind === k} onClick={() => setKind(k)}>
                    {ti(`kind.${k}`)}
                  </ChipButton>
                ))}
              </div>
            </div>
          </div>

          <div className="grid gap-5 sm:grid-cols-2">
            <div className="space-y-2">
              <div className="text-sm font-bold">{t("questionCount")}</div>
              <div className="flex flex-wrap gap-1.5">
                {COUNTS.map((n) => (
                  <ChipButton key={n} active={count === n} onClick={() => setCount(n)}>
                    {tc("questions", { count: n })}
                  </ChipButton>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <div className="text-sm font-bold">{t("timerLabel")}</div>
              <div className="flex flex-wrap gap-1.5">
                {TIMERS.map((sec) => (
                  <ChipButton key={sec} active={timerSec === sec} onClick={() => setTimerSec(sec)}>
                    {sec === 0 ? t("noTimer") : tc("minutes", { count: sec / 60 })}
                  </ChipButton>
                ))}
              </div>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-3 border-t border-border pt-4">
            <span className="font-mono text-xs tabular-nums text-muted-foreground">
              {matchingPool.length > 0 ? t("matchingPool", { count: matchingPool.length }) : t("noMatches")}
            </span>
            <Button size="lg" type="button" disabled={matchingPool.length === 0} onClick={startSession}>
              {t("start")}
              <ArrowRight aria-hidden="true" />
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (phase === "active") {
    const q = queue[pos];
    if (!q) return null;
    const qa = loc.pick(q);
    const timesUp = timerSec > 0 && remainingSec === 0;

    return (
      <div className="space-y-4">
        <div className="flex flex-wrap items-center gap-3">
          <span className="font-mono text-sm font-medium tabular-nums text-foreground">
            {pos + 1}/{queue.length}
          </span>
          <Progress value={pos / queue.length} className="min-w-24 flex-1" />
          {timerSec > 0 && (
            <div className="flex items-center gap-1.5">
              <Badge variant={timesUp ? "danger" : "muted"} className="font-mono tabular-nums">
                <Clock className="size-3.5" aria-hidden="true" />
                {timesUp ? t("timesUp") : formatDuration(remainingSec)}
              </Badge>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => setPaused((p) => !p)}
                aria-label={paused ? t("resume") : t("pause")}
              >
                {paused ? <Play className="size-3.5" aria-hidden="true" /> : <Pause className="size-3.5" aria-hidden="true" />}
              </Button>
            </div>
          )}
          <Button type="button" variant="ghost" size="sm" onClick={() => setPhase("summary")}>
            {t("quit")}
          </Button>
        </div>

        <Card className="animate-rise" key={`${q.id}-${pos}`}>
          <CardContent className="space-y-4 p-6 sm:p-8">
            <div className="flex flex-wrap items-center gap-1.5">
              <Badge variant="muted">{loc.t(catalog.topics[q.topic]) ?? q.topic}</Badge>
              <Badge variant="outline">{ti(`level.${q.level}`)}</Badge>
              {q.kind && <Badge variant="outline">{ti(`kind.${q.kind}`)}</Badge>}
              {qa.fallback && <UntranslatedBadge />}
            </div>

            <div className="text-lg font-bold leading-snug">
              <Markdown text={qa.value!.question} className="[&_p]:m-0" />
            </div>

            {q.code && <StaticCode code={q.code} />}

            {qa.value?.tip && (
              <div>
                <Button type="button" variant="ghost" size="sm" onClick={() => setTipOpen((o) => !o)} className="px-2">
                  <Lightbulb className="size-4 text-primary" aria-hidden="true" />
                  {tipOpen ? t("hideTip") : t("showTip")}
                </Button>
                {tipOpen && (
                  <div className="mt-2 rounded-md border border-border bg-muted/40 p-3 text-sm text-foreground animate-rise">
                    <span className="font-bold text-primary-ink">{ti("tip")}: </span>
                    {qa.value.tip}
                  </div>
                )}
              </div>
            )}

            {!revealed ? (
              <div className="space-y-2 pt-2">
                <label htmlFor={`mock-notes-${q.id}`} className="block text-sm font-bold text-foreground">
                  {t("notesLabel")}
                </label>
                <textarea
                  id={`mock-notes-${q.id}`}
                  rows={4}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder={t("notesPlaceholder")}
                  className="w-full rounded-md border border-border bg-background p-3 text-sm text-foreground placeholder:text-muted-foreground outline-none focus-visible:outline-2 focus-visible:outline-ring"
                />
              </div>
            ) : (
              <div className="space-y-4 border-t border-border pt-4 animate-rise">
                {notes.trim() && (
                  <div className="rounded-md border border-border bg-muted/30 p-3 text-sm">
                    <div className="mb-1 text-xs font-bold text-muted-foreground">{t("yourNotes")}</div>
                    <p className="whitespace-pre-wrap text-foreground">{notes}</p>
                  </div>
                )}
                <div className="space-y-2">
                  <div className="text-xs font-bold uppercase tracking-wide text-primary-ink">{t("modelAnswer")}</div>
                  <Markdown text={qa.value!.answer} />
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {!revealed ? (
          <Button size="lg" type="button" className="w-full" onClick={() => setRevealed(true)}>
            {t("revealAnswer")}
          </Button>
        ) : (
          <Card className="animate-rise">
            <CardContent className="space-y-3 p-5">
              <div className="text-sm font-bold text-foreground">{t("ratePrompt")}</div>
              <div className="grid grid-cols-1 gap-2 sm:grid-cols-3">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => handleRate("needs_work")}
                  className="h-auto flex-col gap-0.5 py-2.5"
                >
                  <span className="font-bold text-danger">{t("rateNeedsWork")}</span>
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => handleRate("partial")}
                  className="h-auto flex-col gap-0.5 py-2.5"
                >
                  <span className="font-bold">{t("ratePartial")}</span>
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => handleRate("confident")}
                  className="h-auto flex-col gap-0.5 border-primary bg-accent/50 py-2.5 text-primary-ink"
                >
                  <span className="font-bold">{t("rateConfident")}</span>
                  <span className="text-xs font-normal text-muted-foreground">{t("confidentHint")}</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    );
  }

  // Summary phase
  const confidentCount = results.filter((r) => r.rating === "confident").length;
  const partialCount = results.filter((r) => r.rating === "partial").length;
  const needsWorkCount = results.filter((r) => r.rating === "needs_work").length;
  const revisit = results.filter((r) => r.rating !== "confident");

  return (
    <div className="space-y-5 animate-rise">
      <Card>
        <CardContent className="flex flex-col items-center gap-4 p-6 text-center sm:p-8">
          <CheckCircle2 className="size-9 text-primary" aria-hidden="true" />
          <div>
            <h2 className="text-xl font-bold">{t("summaryTitle")}</h2>
            <p className="mt-1 font-mono text-sm tabular-nums text-muted-foreground">
              {t("elapsed", { time: formatDuration(elapsedSec) })}
            </p>
          </div>
          <div className="grid w-full max-w-md grid-cols-3 gap-2">
            <div className="rounded-md border border-border bg-success-soft/50 p-3">
              <div className="font-mono text-xl font-bold tabular-nums text-primary-ink">{confidentCount}</div>
              <div className="text-xs text-muted-foreground">{t("rateConfident")}</div>
            </div>
            <div className="rounded-md border border-border bg-muted/40 p-3">
              <div className="font-mono text-xl font-bold tabular-nums text-foreground">{partialCount}</div>
              <div className="text-xs text-muted-foreground">{t("ratePartial")}</div>
            </div>
            <div className="rounded-md border border-border bg-danger-soft/50 p-3">
              <div className="font-mono text-xl font-bold tabular-nums text-danger">{needsWorkCount}</div>
              <div className="text-xs text-muted-foreground">{t("rateNeedsWork")}</div>
            </div>
          </div>
          {revisit.length === 0 && results.length > 0 && (
            <p className="text-sm font-medium text-primary-ink">{t("allConfident")}</p>
          )}
          <div className="flex flex-wrap justify-center gap-3">
            <Button type="button" onClick={() => setPhase("setup")}>
              <RotateCcw aria-hidden="true" />
              {t("newMock")}
            </Button>
            {needsWorkCount > 0 && (
              <Button type="button" variant="outline" onClick={retryNeedsWork}>
                {t("retryMissed", { count: needsWorkCount })}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {revisit.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">{t("revisitTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {revisit.map(({ question, rating }) => {
              const qa = loc.pick(question);
              return (
                <div key={question.id} className="space-y-2 rounded-md border border-border p-4">
                  <div className="flex flex-wrap items-center gap-1.5">
                    <Badge variant={rating === "needs_work" ? "danger" : "muted"}>
                      <AlertCircle className="size-3" aria-hidden="true" />
                      {rating === "needs_work" ? t("rateNeedsWork") : t("ratePartial")}
                    </Badge>
                    <Badge variant="muted">{loc.t(catalog.topics[question.topic]) ?? question.topic}</Badge>
                    <Badge variant="outline">{ti(`level.${question.level}`)}</Badge>
                  </div>
                  <div className="font-bold">
                    <Markdown text={qa.value!.question} className="[&_p]:m-0" />
                  </div>
                  <Markdown text={qa.value!.answer} />
                  {qa.value?.tip && (
                    <div className="rounded-md border border-border bg-muted/40 p-2.5 text-xs text-foreground">
                      <span className="font-bold text-primary-ink">{ti("tip")}: </span>
                      {qa.value.tip}
                    </div>
                  )}
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
