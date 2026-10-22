"use client";

import { ArrowRight, PartyPopper, RotateCcw, Target } from "lucide-react";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { QuestionView } from "@/components/question";
import { Button } from "@/components/ui/button";
import { Progress, Ring } from "@/components/ui/progress";
import { useProgress, type AnswerRecord } from "@/lib/progress";
import { emptyAnswer, grade, isAnswered, type UserAnswer } from "@/lib/quiz";
import { QUIZ_PASS } from "@/lib/selectors";
import type { Flashcard, Question } from "@/lib/types";
import { percent } from "@/lib/utils";

export function LessonQuiz({ lessonId, questions, flashcards, onDone }: { lessonId: string; questions: Question[]; flashcards: Flashcard[]; onDone?: () => void }) {
  const t = useTranslations("quiz");
  const tl = useTranslations("lesson");
  const recordQuiz = useProgress((s) => s.recordQuiz);
  const best = useProgress((s) => s.quizzes[lessonId]?.best);
  const [phase, setPhase] = useState<"intro" | "run" | "result">("intro");
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState<UserAnswer[]>(() => questions.map(emptyAnswer));
  const [revealed, setRevealed] = useState(false);
  const [score, setScore] = useState(0);

  const start = () => {
    setAnswers(questions.map(emptyAnswer));
    setIndex(0);
    setRevealed(false);
    setPhase("run");
  };

  const finish = () => {
    const records: AnswerRecord[] = questions.map((q, i) => ({ questionId: q.id, correct: grade(q, answers[i]), tags: q.tags }));
    const s = records.filter((r) => r.correct).length / questions.length;
    setScore(s);
    recordQuiz(lessonId, s, records, flashcards.map((f) => f.id));
    setPhase("result");
  };

  if (phase === "intro") {
    return (
      <div className="flex flex-col items-center gap-4 py-10 text-center animate-rise">
        <Ring value={best ?? 0} size={88} stroke={7}>
          <span className="text-base">{best !== undefined ? percent(best) : <Target className="size-6 text-primary" />}</span>
        </Ring>
        <div>
          <h2 className="text-xl font-semibold">{t("title")}</h2>
          <p className="mt-1 text-sm text-muted-foreground">{tl("quizPass", { score: percent(QUIZ_PASS) })}</p>
          {best !== undefined && <p className="mt-1 text-sm text-muted-foreground">{tl("quizBest", { score: percent(best) })}</p>}
        </div>
        <Button size="lg" onClick={start}>
          {tl("startQuiz")} <ArrowRight />
        </Button>
      </div>
    );
  }

  if (phase === "result") {
    const passed = score >= QUIZ_PASS;
    return (
      <div className="flex flex-col items-center gap-4 py-10 text-center animate-rise">
        <Ring value={score} size={110} stroke={8}>
          <span className="text-xl">{percent(score)}</span>
        </Ring>
        {passed && <PartyPopper className="size-7 text-warning" />}
        <div>
          <h2 className="text-xl font-semibold">{t("result", { score: percent(score) })}</h2>
          <p className="mt-1 max-w-sm text-sm text-muted-foreground">{passed ? t("resultPass") : t("resultFail", { score: percent(QUIZ_PASS) })}</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={start}>
            <RotateCcw /> {t("restart")}
          </Button>
          {onDone && <Button onClick={onDone}>{t("backToLesson")}</Button>}
        </div>
      </div>
    );
  }

  const q = questions[index];
  const a = answers[index];
  const last = index === questions.length - 1;
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <span className="text-xs font-medium text-muted-foreground">{t("question", { n: index + 1, total: questions.length })}</span>
        <Progress value={(index + (revealed ? 1 : 0)) / questions.length} className="flex-1" />
      </div>
      <div key={q.id} className="animate-rise">
        <QuestionView question={q} answer={a} revealed={revealed} onChange={(na) => setAnswers((all) => all.map((x, i) => (i === index ? na : x)))} />
      </div>
      <div className="flex justify-end">
        {!revealed ? (
          <Button onClick={() => setRevealed(true)} disabled={!isAnswered(q, a)}>
            {t("check")}
          </Button>
        ) : last ? (
          <Button onClick={finish}>
            {t("finish")} <ArrowRight />
          </Button>
        ) : (
          <Button
            onClick={() => {
              setIndex(index + 1);
              setRevealed(false);
            }}
          >
            {t("next")} <ArrowRight />
          </Button>
        )}
      </div>
    </div>
  );
}
