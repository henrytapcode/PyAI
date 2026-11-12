"use client";

import {
  AlertTriangle,
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  Clock,
  Flag,
  RotateCcw,
  Timer,
  XCircle,
} from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { QuestionView } from "@/components/question";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog";
import { Progress, Ring } from "@/components/ui/progress";
import { catalog } from "@/lib/content";
import { Tx, useLoc } from "@/lib/i18n";
import { useProgress, type AnswerRecord } from "@/lib/progress";
import { emptyAnswer, grade, isAnswered, type UserAnswer } from "@/lib/quiz";
import type { Exam } from "@/lib/types";
import { cn, formatDuration, percent, todayKey } from "@/lib/utils";

type Phase = "intro" | "run" | "result";

export function ExamRunner({ exam, onFinished, backHref = "/exams/" }: { exam: Exam; onFinished?: (passed: boolean) => void; backHref?: string }) {
  const t = useTranslations("exam");
  const tc = useTranslations("common");
  const loc = useLoc();
  const history = useProgress((s) => s.exams[exam.id]);
  const recordExam = useProgress((s) => s.recordExam);

  const [phase, setPhase] = useState<Phase>("intro");
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<UserAnswer[]>(() => exam.questions.map(emptyAnswer));
  const [deadline, setDeadline] = useState(0);
  const [now, setNow] = useState(() => Date.now());
  const [startedAt, setStartedAt] = useState(0);
  const [confirm, setConfirm] = useState(false);
  const [timeUp, setTimeUp] = useState(false);
  const [result, setResult] = useState<{ score: number; passed: boolean; byTopic: Record<string, { correct: number; total: number }>; correct: boolean[] } | null>(null);
  const submitted = useRef(false);

  const start = () => {
    submitted.current = false;
    setAnswers(exam.questions.map(emptyAnswer));
    setIndex(0);
    setTimeUp(false);
    const t0 = Date.now();
    setStartedAt(t0);
    setNow(t0);
    setDeadline(t0 + exam.duration_min * 60_000);
    setPhase("run");
  };

  const submit = useCallback(() => {
    if (submitted.current) return;
    submitted.current = true;
    const correct = exam.questions.map((q, i) => grade(q, answers[i]));
    const byTopic: Record<string, { correct: number; total: number }> = {};
    exam.questions.forEach((q, i) => {
      const topic = q.tags[0];
      byTopic[topic] ??= { correct: 0, total: 0 };
      byTopic[topic].total += 1;
      if (correct[i]) byTopic[topic].correct += 1;
    });
    const score = correct.filter(Boolean).length / exam.questions.length;
    const passed = score >= exam.pass_score;
    const records: AnswerRecord[] = exam.questions.map((q, i) => ({ questionId: q.id, correct: correct[i], tags: q.tags }));
    recordExam(
      exam.id,
      { date: todayKey(), score, passed, durationSec: Math.round((Date.now() - startedAt) / 1000), byTopic },
      records,
      exam.skips_phases,
      exam.kind === "placement",
    );
    setResult({ score, passed, byTopic, correct });
    setConfirm(false);
    setPhase("result");
    onFinished?.(passed);
  }, [answers, exam, onFinished, recordExam, startedAt]);

  // Timer
  useEffect(() => {
    if (phase !== "run") return;
    const id = setInterval(() => setNow(Date.now()), 500);
    return () => clearInterval(id);
  }, [phase]);
  const remaining = Math.max(0, (deadline - now) / 1000);
  useEffect(() => {
    if (phase === "run" && remaining <= 0) {
      setTimeUp(true);
      submit();
    }
  }, [phase, remaining, submit]);

  const answeredCount = useMemo(() => exam.questions.filter((q, i) => isAnswered(q, answers[i])).length, [answers, exam.questions]);
  const best = history?.length ? Math.max(...history.map((h) => h.score)) : undefined;

  if (phase === "intro") {
    return (
      <Card className="mx-auto max-w-2xl animate-rise">
        <CardContent className="space-y-6 p-8">
          <div>
            <Badge variant="muted">{exam.kind === "placement" ? t("placement") : exam.kind === "mock" ? t("mocks") : t("phaseTests")}</Badge>
            <h1 className="mt-3 text-2xl font-bold tracking-tight">
              <Tx value={exam.title} />
            </h1>
            {exam.description && <p className="mt-2 text-muted-foreground">{loc.t(exam.description)}</p>}
          </div>
          <div className="flex flex-wrap gap-3 text-sm">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-muted px-3 py-1.5 tabular-nums">
              <Flag className="size-4 text-muted-foreground" aria-hidden="true" />
              {tc("questions", { count: exam.questions.length })}
            </span>
            <span className="inline-flex items-center gap-1.5 rounded-full bg-muted px-3 py-1.5 tabular-nums">
              <Clock className="size-4 text-muted-foreground" aria-hidden="true" />
              {t("duration", { count: exam.duration_min })}
            </span>
            <span className="inline-flex items-center gap-1.5 rounded-full bg-muted px-3 py-1.5 tabular-nums">
              <CheckCircle2 className="size-4 text-muted-foreground" aria-hidden="true" />
              {t("passScore", { score: percent(exam.pass_score) })}
            </span>
          </div>
          <p className="text-sm text-muted-foreground">{t("rules")}</p>
          {history && history.length > 0 && (
            <div>
              <div className="mb-2 text-sm font-bold">{t("history")}</div>
              <div className="flex flex-wrap gap-2">
                {history.slice(-6).map((h, i) => (
                  <Badge key={i} variant={h.passed ? "success" : "muted"} className="font-mono tabular-nums">
                    {h.date} · {percent(h.score)}
                  </Badge>
                ))}
              </div>
            </div>
          )}
          <div className="flex items-center gap-3">
            <Button size="lg" onClick={start}>
              <Timer className="size-4" aria-hidden="true" /> {t("start")}
            </Button>
            {best !== undefined && <span className="text-sm text-muted-foreground">{t("best", { score: percent(best) })}</span>}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (phase === "result" && result) {
    return (
      <div className="mx-auto max-w-3xl space-y-6 animate-rise">
        {timeUp && (
          <div className="flex items-center gap-2.5 rounded-lg border border-warning/40 bg-warning-soft px-4 py-3 text-sm text-foreground">
            <AlertTriangle className="size-5 shrink-0 text-warning-ink" aria-hidden="true" />
            <span>{t("timeUp")}</span>
          </div>
        )}
        <Card>
          <CardContent className="flex flex-wrap items-center gap-6 p-8">
            <Ring value={result.score} size={120} stroke={9}>
              <span className="font-mono text-3xl font-bold tabular-nums">{percent(result.score)}</span>
            </Ring>
            <div className="min-w-0 flex-1">
              <div className="text-sm text-muted-foreground">{t("report")}</div>
              <h1 className="text-2xl font-bold">
                <Tx value={exam.title} />
              </h1>
              <Badge className="mt-2" variant={result.passed ? "success" : "danger"}>
                {result.passed ? (
                  <CheckCircle2 className="size-4" aria-hidden="true" />
                ) : (
                  <XCircle className="size-4" aria-hidden="true" />
                )}
                {result.passed ? t("passed") : t("failed")} · {t("passScore", { score: percent(exam.pass_score) })}
              </Badge>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={start}>
                <RotateCcw className="size-4" aria-hidden="true" /> {t("retake")}
              </Button>
              <Button asChild>
                <Link href={backHref}>{tc("done")}</Link>
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="space-y-4 p-6">
            <h2 className="text-lg font-bold">{t("byTopic")}</h2>
            {Object.entries(result.byTopic)
              .sort(([, a], [, b]) => a.correct / a.total - b.correct / b.total)
              .map(([topic, v]) => (
                <div key={topic} className="space-y-1.5">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium text-foreground">{loc.t(catalog.topics[topic]) ?? topic}</span>
                    <span className="font-mono tabular-nums text-muted-foreground">
                      {v.correct}/{v.total}
                    </span>
                  </div>
                  <Progress value={v.correct / v.total} tone={v.correct / v.total >= exam.pass_score ? "success" : "primary"} />
                </div>
              ))}
          </CardContent>
        </Card>

        <div className="space-y-4">
          <h2 className="text-lg font-bold">{t("review")}</h2>
          {exam.questions.map((q, i) => (
            <Card key={q.id}>
              <CardContent className="p-6">
                <div className="mb-3 flex items-center gap-2.5 text-xs">
                  {result.correct[i] ? (
                    <span className="flex items-center gap-1 font-medium text-primary">
                      <CheckCircle2 className="size-4 text-primary" aria-hidden="true" />
                      {t("correct")}
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 font-medium text-danger">
                      <XCircle className="size-4 text-danger" aria-hidden="true" />
                      {t("incorrect")}
                    </span>
                  )}
                  <span className="font-mono tabular-nums text-muted-foreground">#{i + 1}</span>
                  {!isAnswered(q, answers[i]) && <Badge variant="muted">{t("unanswered")}</Badge>}
                </div>
                <QuestionView question={q} answer={answers[i]} onChange={() => {}} revealed />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  const q = exam.questions[index];
  const lowTime = remaining < 60;
  return (
    <div className="mx-auto max-w-3xl">
      <div className="sticky top-14 z-20 -mx-4 mb-6 border-b border-border bg-background px-4 py-3 lg:top-0">
        <div className="flex items-center gap-3">
          <div
            className={cn(
              "flex shrink-0 items-center gap-1.5 rounded-md px-3 py-1.5 font-mono text-sm font-bold tabular-nums",
              lowTime ? "bg-warning-soft text-warning-ink" : "bg-muted text-foreground",
            )}
            aria-live="polite"
          >
            {lowTime ? (
              <AlertTriangle className="size-4 shrink-0 text-warning-ink" aria-hidden="true" />
            ) : (
              <Timer className="size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
            )}
            {formatDuration(remaining)}
            {lowTime && <span className="sr-only">({t("timeLeft")})</span>}
          </div>
          <span className="text-xs font-mono tabular-nums text-muted-foreground sm:text-sm">
            {t("answered", { done: answeredCount, total: exam.questions.length })}
          </span>
          <Button className="ml-auto shrink-0" size="sm" onClick={() => setConfirm(true)}>
            {t("submit")}
          </Button>
        </div>
        <div className="mt-3 flex flex-wrap gap-1.5">
          {exam.questions.map((qq, i) => {
            const answered = isAnswered(qq, answers[i]);
            const current = i === index;
            return (
              <button
                key={qq.id}
                type="button"
                onClick={() => setIndex(i)}
                aria-current={current ? "true" : undefined}
                aria-label={t("questionNumber", { n: i + 1 })}
                className={cn(
                  "grid size-9 place-items-center rounded-md font-mono text-xs font-bold transition-colors",
                  current
                    ? "border-2 border-primary" + (answered ? " bg-accent text-primary" : " bg-card text-foreground")
                    : answered
                      ? "border border-primary/40 bg-accent text-primary"
                      : "border border-border bg-card text-muted-foreground hover:bg-muted hover:text-foreground",
                )}
              >
                {i + 1}
              </button>
            );
          })}
        </div>
      </div>

      <Card key={q.id} className="animate-rise">
        <CardContent className="p-6 sm:p-8">
          <QuestionView question={q} answer={answers[index]} revealed={false} onChange={(a) => setAnswers((all) => all.map((x, i) => (i === index ? a : x)))} />
        </CardContent>
      </Card>

      <div className="mt-4 flex justify-between">
        <Button variant="outline" disabled={index === 0} onClick={() => setIndex(index - 1)}>
          <ArrowLeft className="size-4" aria-hidden="true" /> {tc("previous")}
        </Button>
        {index < exam.questions.length - 1 ? (
          <Button variant="outline" onClick={() => setIndex(index + 1)}>
            {tc("next")} <ArrowRight className="size-4" aria-hidden="true" />
          </Button>
        ) : (
          <Button onClick={() => setConfirm(true)}>{t("submit")}</Button>
        )}
      </div>

      <Dialog open={confirm} onOpenChange={setConfirm}>
        <DialogContent>
          <DialogTitle>{t("submit")}</DialogTitle>
          <DialogDescription>{t("submitConfirm", { count: exam.questions.length - answeredCount })}</DialogDescription>
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setConfirm(false)}>
              {tc("cancel")}
            </Button>
            <Button onClick={submit}>{t("submit")}</Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
