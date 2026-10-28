"use client";

import { CheckCircle2, Layers, PartyPopper, RotateCcw } from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { useMemo, useState } from "react";
import reviewJson from "@/generated/review.json";
import { Markdown, StaticCode } from "@/components/markdown";
import { PageHeader } from "@/components/page-header";
import { QuestionView } from "@/components/question";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { findLesson } from "@/lib/content";
import { UntranslatedBadge, useLoc } from "@/lib/i18n";
import { useProgress } from "@/lib/progress";
import { emptyAnswer, grade as gradeAnswer, isAnswered, type UserAnswer } from "@/lib/quiz";
import { dueKeys } from "@/lib/selectors";
import { newCard, previewInterval, type Grade } from "@/lib/srs";
import type { Flashcard, Question } from "@/lib/types";
import { cn, shuffle } from "@/lib/utils";

const deck = reviewJson as unknown as { flashcards: Flashcard[]; questions: Question[] };
const cardsById = new Map(deck.flashcards.map((c) => [c.id, c]));
const questionsById = new Map(deck.questions.map((q) => [q.id, q]));

function resolve(key: string) {
  if (key.startsWith("card:")) {
    const c = cardsById.get(key.slice(5));
    return c ? ({ kind: "card", item: c } as const) : null;
  }
  const q = questionsById.get(key.slice(2));
  return q ? ({ kind: "question", item: q } as const) : null;
}

export default function ReviewPage() {
  const t = useTranslations("review");
  const p = useProgress();
  const reviewCard = useProgress((s) => s.reviewCard);
  const initialDue = useMemo(() => dueKeys(p).filter((k) => resolve(k)), []); // eslint-disable-line react-hooks/exhaustive-deps
  const [queue, setQueue] = useState<string[]>(initialDue);
  const [pos, setPos] = useState(0);
  const [reviewed, setReviewed] = useState(0);
  const deckSize = Object.keys(p.srs).length;

  const key = queue[pos];
  const entry = key ? resolve(key) : null;

  const onGrade = (g: Grade) => {
    reviewCard(key, g);
    setReviewed((n) => n + 1);
    // "Again" puts the card back at the end of today's queue.
    if (g === "again") setQueue((q) => [...q, key]);
    setPos((i) => i + 1);
  };

  const practice = () => {
    const keys = shuffle(Object.keys(p.srs).filter((k) => resolve(k))).slice(0, 10);
    setQueue(keys);
    setPos(0);
  };

  return (
    <div className="mx-auto max-w-2xl">
      <PageHeader
        title={t("title")}
        subtitle={t("subtitle")}
        actions={
          <Badge variant="muted">
            <Layers /> {t("deckSize", { count: deckSize })}
          </Badge>
        }
      />

      {!entry ? (
        <Card className="animate-rise">
          <CardContent className="flex flex-col items-center gap-4 p-10 text-center">
            {reviewed > 0 ? <PartyPopper className="size-10 text-warning" /> : <CheckCircle2 className="size-10 text-success" />}
            <div>
              <h2 className="text-lg font-bold">{reviewed > 0 ? t("sessionDone") : t("due", { count: 0 })}</h2>
              <p className="mt-1 text-sm text-muted-foreground">{reviewed > 0 ? t("reviewed", { count: reviewed }) : t("empty")}</p>
            </div>
            {deckSize > 0 && (
              <Button variant="outline" onClick={practice}>
                <RotateCcw /> {t("practice")}
              </Button>
            )}
          </CardContent>
        </Card>
      ) : (
        <>
          <div className="mb-4 flex items-center gap-3 text-sm text-muted-foreground">
            <span className="tabular-nums">
              {Math.min(pos + 1, queue.length)}/{queue.length}
            </span>
            <Progress value={pos / queue.length} className="flex-1" />
          </div>
          {entry.kind === "card" ? (
            <FlashcardView key={`${key}-${pos}`} card={entry.item} cardKey={key} onGrade={onGrade} />
          ) : (
            <QuestionReview key={`${key}-${pos}`} question={entry.item} cardKey={key} onGrade={onGrade} />
          )}
        </>
      )}
    </div>
  );
}

function SourceLine({ lessonId, label }: { lessonId?: string; label: string }) {
  const t = useTranslations("review");
  const loc = useLoc();
  const lesson = lessonId ? findLesson(lessonId) : undefined;
  return (
    <div className="flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
      <Badge variant="muted">{label}</Badge>
      {lesson && (
        <Link href={`/lesson/${lesson.id}/`} className="hover:text-foreground hover:underline">
          {t("fromLesson", { lesson: loc.t(lesson.title) })}
        </Link>
      )}
    </div>
  );
}

function GradeButtons({ cardKey, onGrade, suggest }: { cardKey: string; onGrade: (g: Grade) => void; suggest?: Grade }) {
  const t = useTranslations("review");
  const card = useProgress((s) => s.srs[cardKey]) ?? newCard();
  const grades: { g: Grade; cls: string }[] = [
    { g: "again", cls: "border-danger/40 text-danger hover:bg-danger-soft" },
    { g: "hard", cls: "border-warning/50 text-warning hover:bg-warning-soft" },
    { g: "good", cls: "border-primary/40 text-primary hover:bg-accent" },
    { g: "easy", cls: "border-success/40 text-success hover:bg-success-soft" },
  ];
  return (
    <div className="grid grid-cols-4 gap-2 animate-rise">
      {grades.map(({ g, cls }) => (
        <button
          key={g}
          onClick={() => onGrade(g)}
          className={cn("flex flex-col items-center gap-0.5 rounded-[4px] border bg-card px-2 py-2.5 text-sm font-medium transition", cls, suggest === g && "ring-2 ring-current")}
        >
          {t(g)}
          <span className="text-[11px] font-normal text-muted-foreground">{t("inDays", { count: previewInterval(card, g) })}</span>
        </button>
      ))}
    </div>
  );
}

function FlashcardView({ card, cardKey, onGrade }: { card: Flashcard; cardKey: string; onGrade: (g: Grade) => void }) {
  const t = useTranslations("review");
  const loc = useLoc();
  const [flipped, setFlipped] = useState(false);
  const side = loc.pick(card);
  return (
    <div className="space-y-4">
      <Card className="animate-rise">
        <CardContent className="space-y-5 p-8">
          <SourceLine lessonId={card.lessonId} label={t("flashcard")} />
          <div className="text-xl font-bold">
            <Markdown text={side.value!.front} className="[&_p]:m-0" />
            {side.fallback && <UntranslatedBadge />}
          </div>
          {card.code && <StaticCode code={card.code} />}
          {flipped && (
            <div className="border-t pt-5 animate-rise">
              <Markdown text={side.value!.back} />
            </div>
          )}
        </CardContent>
      </Card>
      {flipped ? (
        <GradeButtons cardKey={cardKey} onGrade={onGrade} />
      ) : (
        <Button size="lg" className="w-full" onClick={() => setFlipped(true)}>
          {t("showAnswer")}
        </Button>
      )}
    </div>
  );
}

function QuestionReview({ question, cardKey, onGrade }: { question: Question; cardKey: string; onGrade: (g: Grade) => void }) {
  const t = useTranslations("review");
  const tq = useTranslations("quiz");
  const [answer, setAnswer] = useState<UserAnswer>(() => emptyAnswer(question));
  const [revealed, setRevealed] = useState(false);
  const correct = revealed && gradeAnswer(question, answer);
  return (
    <div className="space-y-4">
      <Card className="animate-rise">
        <CardContent className="space-y-4 p-8">
          <SourceLine lessonId={question.lessonId} label={t("missedQuestion")} />
          <QuestionView question={question} answer={answer} onChange={setAnswer} revealed={revealed} showType={false} />
        </CardContent>
      </Card>
      {revealed ? (
        <GradeButtons cardKey={cardKey} onGrade={onGrade} suggest={correct ? "good" : "again"} />
      ) : (
        <Button size="lg" className="w-full" disabled={!isAnswered(question, answer)} onClick={() => setRevealed(true)}>
          {tq("check")}
        </Button>
      )}
    </div>
  );
}
