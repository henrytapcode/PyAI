"use client";

import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  ChevronLeft,
  Clock,
  Code2,
  ExternalLink,
  FlaskConical,
  ListChecks,
  PartyPopper,
  PenLine,
  Sparkles,
} from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useRef, useState } from "react";
import { ExercisePanel, ExercisePicker } from "@/components/lesson/exercise-panel";
import { LessonQuiz } from "@/components/lesson/lesson-quiz";
import { Markdown } from "@/components/markdown";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Workbench } from "@/components/workbench";
import { findLesson, neighbours, phaseOfLesson } from "@/lib/content";
import { Tx, UntranslatedBadge, useLoc } from "@/lib/i18n";
import { useProgress } from "@/lib/progress";
import { isLessonComplete, lessonParts } from "@/lib/selectors";
import type { Lesson, TestRunResult } from "@/lib/types";
import { cn, percent } from "@/lib/utils";

type Tab = "theory" | "examples" | "exercises" | "quiz";

export function LessonView({ lesson }: { lesson: Lesson }) {
  const t = useTranslations("lesson");
  const tc = useTranslations("common");
  const te = useTranslations("exercise");
  const loc = useLoc();
  const { meta } = lesson;
  const summary = findLesson(meta.id)!;
  const phase = phaseOfLesson(meta.id);
  const { prev, next } = neighbours(meta.id);

  const p = useProgress();
  const visitLesson = useProgress((s) => s.visitLesson);
  const markTheory = useProgress((s) => s.markTheory);
  const saveCode = useProgress((s) => s.saveCode);
  const recordCheck = useProgress((s) => s.recordCheck);
  const markLessonComplete = useProgress((s) => s.markLessonComplete);

  const [tab, setTab] = useState<Tab>("theory");
  const [exerciseId, setExerciseId] = useState<string | null>(lesson.exercises[0]?.id ?? null);
  const [scratch, setScratch] = useState<string>(lesson.examples[0]?.code ?? "print('Hello, AI engineer!')\n");
  const [mobilePane, setMobilePane] = useState<"content" | "editor">("content");
  const [celebrate, setCelebrate] = useState(false);
  const exercise = lesson.exercises.find((e) => e.id === exerciseId) ?? null;
  const editingExercise = tab === "exercises" && exercise;

  useEffect(() => {
    visitLesson(meta.id);
  }, [meta.id, visitLesson]);

  // Celebrate once when the lesson becomes complete.
  const complete = isLessonComplete(p, summary);
  const wasComplete = useRef(complete);
  useEffect(() => {
    if (complete && !wasComplete.current) {
      markLessonComplete(meta.id);
      setCelebrate(true);
    }
    wasComplete.current = complete;
  }, [complete, markLessonComplete, meta.id]);

  // Debounced autosave of exercise code.
  const [exCode, setExCode] = useState<string>("");
  useEffect(() => {
    if (exercise) setExCode(useProgress.getState().exercises[exercise.id]?.code ?? exercise.starter);
  }, [exercise]);
  const saveTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  const onExCode = useCallback(
    (code: string) => {
      setExCode(code);
      if (!exercise) return;
      clearTimeout(saveTimer.current);
      saveTimer.current = setTimeout(() => saveCode(exercise.id, code), 400);
    },
    [exercise, saveCode],
  );

  const tryCode = (code: string) => {
    setScratch(code);
    if (tab === "exercises") setTab("theory");
    setMobilePane("editor");
  };

  const parts = lessonParts(p, summary);
  const body = loc.pick(lesson.body);
  const outcomes = loc.t(meta.outcomes);

  // Resizable split (desktop).
  const [split, setSplit] = useState(50);
  const container = useRef<HTMLDivElement>(null);
  const startDrag = (e: React.PointerEvent) => {
    e.preventDefault();
    const rect = container.current?.getBoundingClientRect();
    if (!rect) return;
    const move = (ev: PointerEvent) => setSplit(Math.min(70, Math.max(30, ((ev.clientX - rect.left) / rect.width) * 100)));
    const up = () => {
      window.removeEventListener("pointermove", move);
      window.removeEventListener("pointerup", up);
    };
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", up);
  };

  const onTestResult = (r: TestRunResult) => {
    if (exercise && !r.timedOut) recordCheck(exercise.id, r.passed, r.total);
  };

  return (
    <div className="flex h-[calc(100dvh-3.5rem-4rem)] flex-col lg:h-dvh">
      {/* Lesson header */}
      <header className="flex items-center gap-3 border-b bg-background/90 px-4 py-2.5 backdrop-blur">
        <Button asChild variant="ghost" size="icon-sm" aria-label={tc("back")}>
          <Link href="/learn/">
            <ChevronLeft />
          </Link>
        </Button>
        <div className="min-w-0 flex-1">
          <div className="truncate text-xs text-muted-foreground">
            {loc.t(phase?.title)} · {meta.kind === "project" ? t("projectBadge") : `${summary.order}`}
          </div>
          <h1 className="truncate font-semibold leading-tight">
            <Tx value={meta.title} />
          </h1>
        </div>
        <div className="hidden items-center gap-1.5 md:flex">
          <StepChip done={parts.theory} icon={<BookOpen className="size-3.5" />} label={t("theory")} onClick={() => setTab("theory")} />
          <StepChip
            done={parts.exTotal > 0 && parts.exPassed === parts.exTotal}
            icon={<PenLine className="size-3.5" />}
            label={`${t("exercises")} ${parts.exPassed}/${parts.exTotal}`}
            onClick={() => setTab("exercises")}
          />
          <StepChip
            done={parts.quizDone}
            icon={<ListChecks className="size-3.5" />}
            label={`${t("quiz")}${parts.quizBest ? ` ${percent(parts.quizBest)}` : ""}`}
            onClick={() => setTab("quiz")}
          />
        </div>
        <div className="flex items-center">
          <Button asChild={!!prev} variant="ghost" size="icon-sm" disabled={!prev} aria-label={t("prevLesson")}>
            {prev ? (
              <Link href={`/lesson/${prev.id}/`}>
                <ArrowLeft />
              </Link>
            ) : (
              <ArrowLeft />
            )}
          </Button>
          <Button asChild={!!next} variant="ghost" size="icon-sm" disabled={!next} aria-label={t("nextLesson")}>
            {next ? (
              <Link href={`/lesson/${next.id}/`}>
                <ArrowRight />
              </Link>
            ) : (
              <ArrowRight />
            )}
          </Button>
        </div>
      </header>

      {/* Mobile pane switch */}
      <div className="flex gap-1 border-b p-2 lg:hidden">
        {(["content", "editor"] as const).map((pane) => (
          <button
            key={pane}
            onClick={() => setMobilePane(pane)}
            className={cn(
              "flex flex-1 items-center justify-center gap-1.5 rounded-lg py-1.5 text-sm font-medium",
              mobilePane === pane ? "bg-accent text-accent-foreground" : "text-muted-foreground",
            )}
          >
            {pane === "content" ? <BookOpen className="size-4" /> : <Code2 className="size-4" />}
            {pane === "content" ? t("content") : t("editor")}
          </button>
        ))}
      </div>

      <div ref={container} className="flex min-h-0 flex-1">
        {/* Left: content */}
        <section
          style={{ ["--split" as string]: `${split}%` }}
          className={cn("min-h-0 w-full overflow-y-auto lg:block lg:w-[var(--split)]", mobilePane === "content" ? "block" : "hidden")}
        >
          <Tabs value={tab} onValueChange={(v) => setTab(v as Tab)} className="mx-auto max-w-3xl px-5 py-5 sm:px-8">
            <TabsList className="sticky top-0 z-10 mb-6 w-full justify-start overflow-x-auto shadow-sm">
              <TabsTrigger value="theory">
                <BookOpen /> {t("theory")}
                {parts.theory && <CheckCircle2 className="text-success" />}
              </TabsTrigger>
              <TabsTrigger value="examples">
                <Sparkles /> {t("examples")}
              </TabsTrigger>
              <TabsTrigger value="exercises">
                <PenLine /> {t("exercises")}
                <span className="text-xs text-muted-foreground">
                  {parts.exPassed}/{parts.exTotal}
                </span>
              </TabsTrigger>
              <TabsTrigger value="quiz">
                <ListChecks /> {t("quiz")}
                {parts.quizDone && <CheckCircle2 className="text-success" />}
              </TabsTrigger>
            </TabsList>

            <TabsContent value="theory" className="space-y-8 animate-rise">
              <div className="rounded-2xl border bg-accent/30 p-5">
                <div className="mb-2 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
                  <Clock className="size-3.5" /> {tc("minutes", { count: meta.duration_min })}
                  {meta.kind === "project" && <Badge>{t("projectBadge")}</Badge>}
                </div>
                <p className="mb-3 text-[0.95rem]">{loc.t(meta.summary)}</p>
                <div className="text-sm font-semibold">{t("outcomes")}</div>
                <ul className="mt-1.5 space-y-1 text-sm">
                  {outcomes.map((o) => (
                    <li key={o} className="flex gap-2">
                      <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-primary" />
                      {o}
                    </li>
                  ))}
                </ul>
              </div>

              {body.fallback && <UntranslatedBadge />}
              <Markdown text={body.value ?? ""} onTryCode={tryCode} />

              <div className="flex flex-wrap items-center gap-3 rounded-2xl border p-5">
                {parts.theory ? (
                  <span className="flex items-center gap-2 font-medium text-success">
                    <CheckCircle2 className="size-5" /> {t("read")}
                  </span>
                ) : (
                  <Button onClick={() => markTheory(meta.id, lesson.quiz.flashcards.map((f) => f.id))}>
                    <CheckCircle2 /> {t("markRead")}
                  </Button>
                )}
                <Button variant="outline" className="ml-auto" onClick={() => setTab(lesson.exercises.length ? "exercises" : "quiz")}>
                  {lesson.exercises.length ? t("exercises") : t("quiz")} <ArrowRight />
                </Button>
              </div>

              {meta.further_reading && meta.further_reading.length > 0 && (
                <div className="space-y-1 text-sm">
                  {meta.further_reading.map((fr) => (
                    <a key={fr.url} href={fr.url} target="_blank" rel="noreferrer" className="flex items-center gap-1.5 text-primary hover:underline">
                      <ExternalLink className="size-3.5" />
                      {loc.t(fr.title)}
                    </a>
                  ))}
                </div>
              )}
              <p className="text-xs text-muted-foreground">{t("reviewBy", { date: meta.review_by })}</p>
            </TabsContent>

            <TabsContent value="examples" className="space-y-8 animate-rise">
              {lesson.examples.map((ex) => (
                <div key={ex.name} className="space-y-2">
                  <h3 className="font-semibold">{loc.t(ex.title)}</h3>
                  <Markdown text={"```python\n" + ex.code.replace(/\n$/, "") + "\n```"} onTryCode={tryCode} />
                  {ex.output && (
                    <div>
                      <div className="mb-1 text-xs font-medium uppercase tracking-wide text-muted-foreground">{t("expectedOutput")}</div>
                      <pre className="overflow-x-auto rounded-xl border border-dashed bg-muted/40 p-3 font-mono text-[13px]">{ex.output}</pre>
                    </div>
                  )}
                  {loc.t(ex.explain) && <Markdown text={loc.t(ex.explain)} className="pt-1" />}
                </div>
              ))}
            </TabsContent>

            <TabsContent value="exercises" className="space-y-6 animate-rise">
              <ExercisePicker exercises={lesson.exercises} activeId={exerciseId} onPick={(id) => setExerciseId(id)} />
              {exercise && (
                <ExercisePanel
                  key={exercise.id}
                  exercise={exercise}
                  onLoadCode={(code) => {
                    onExCode(code);
                    setMobilePane("editor");
                  }}
                />
              )}
              {exercise && (
                <Button className="w-full lg:hidden" onClick={() => setMobilePane("editor")}>
                  <Code2 /> {t("editor")}
                </Button>
              )}
            </TabsContent>

            <TabsContent value="quiz" className="animate-rise">
              <LessonQuiz lessonId={meta.id} questions={lesson.quiz.questions} flashcards={lesson.quiz.flashcards} onDone={() => setTab("theory")} />
            </TabsContent>
          </Tabs>
        </section>

        {/* Splitter */}
        <div
          role="separator"
          aria-orientation="vertical"
          onPointerDown={startDrag}
          className="group hidden w-1.5 shrink-0 cursor-col-resize items-center justify-center border-x bg-muted/40 hover:bg-primary/20 lg:flex"
        >
          <div className="h-8 w-0.5 rounded-full bg-muted-foreground/30 group-hover:bg-primary" />
        </div>

        {/* Right: editor */}
        <section className={cn("min-h-0 min-w-0 flex-1 flex-col lg:flex", mobilePane === "editor" ? "flex" : "hidden")}>
          {editingExercise ? (
            <Workbench
              key={exercise.id}
              title={
                <span className="flex items-center gap-2">
                  <FlaskConical className="size-4 text-primary" />
                  <Tx value={exercise.title} />
                </span>
              }
              code={exCode}
              onCodeChange={onExCode}
              tests={exercise.tests}
              onTestResult={onTestResult}
              onReset={() => {
                if (window.confirm(te("resetConfirm"))) onExCode(exercise.starter);
              }}
              highlightBlanks={exercise.kind === "fill"}
              className="h-full"
            />
          ) : (
            <Workbench
              title={
                <span className="flex items-center gap-2 text-muted-foreground">
                  <Code2 className="size-4" /> main.py
                </span>
              }
              code={scratch}
              onCodeChange={setScratch}
              className="h-full"
            />
          )}
        </section>
      </div>

      <Dialog open={celebrate} onOpenChange={setCelebrate}>
        <DialogContent className="text-center">
          <PartyPopper className="mx-auto size-10 text-warning" />
          <DialogTitle className="text-center">{t("lessonComplete")}</DialogTitle>
          <DialogDescription className="text-center">
            <Tx value={meta.title} />
          </DialogDescription>
          <div className="flex justify-center gap-2">
            <Button variant="outline" onClick={() => setCelebrate(false)}>
              {tc("close")}
            </Button>
            {next && (
              <Button asChild>
                <Link href={`/lesson/${next.id}/`}>
                  {t("nextLesson")} <ArrowRight />
                </Link>
              </Button>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}

function StepChip({ done, icon, label, onClick }: { done: boolean; icon: React.ReactNode; label: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium transition hover:bg-muted",
        done && "border-success/40 bg-success-soft text-success",
      )}
    >
      {done ? <CheckCircle2 className="size-3.5" /> : icon}
      {label}
    </button>
  );
}
