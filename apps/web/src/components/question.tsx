"use client";

import { CheckCircle2, GripVertical, XCircle } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useMemo } from "react";
import { Markdown, StaticCode } from "@/components/markdown";
import { Badge } from "@/components/ui/badge";
import { UntranslatedBadge, useLoc } from "@/lib/i18n";
import { correctAnswerText, grade, type UserAnswer } from "@/lib/quiz";
import type { Question } from "@/lib/types";
import { cn, shuffle } from "@/lib/utils";

function seedOf(id: string) {
  let h = 0;
  for (const ch of id) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return h % 2 ** 31;
}

/** Inline markdown for short strings (prompts, options) without paragraph spacing. */
function Inline({ text }: { text: string }) {
  return <Markdown text={text} className="[&_p]:m-0 leading-relaxed" />;
}

export function QuestionView({
  question,
  answer,
  onChange,
  revealed,
  showType = true,
}: {
  question: Question;
  answer: UserAnswer;
  onChange: (a: UserAnswer) => void;
  revealed: boolean;
  showType?: boolean;
}) {
  const t = useTranslations("quiz");
  const loc = useLoc();
  const text = loc.pick(question);
  const qt = text.value!;
  const correct = revealed ? grade(question, answer) : null;

  // Cabinet keys: A to D (or 1 to 4) pick an option while no field has focus.
  const optionCount = question.type === "mcq" ? (qt.options ?? []).length : 0;
  useEffect(() => {
    if (question.type !== "mcq" || revealed) return;
    const onKey = (e: KeyboardEvent) => {
      const el = e.target as HTMLElement | null;
      if (e.metaKey || e.ctrlKey || e.altKey || el instanceof HTMLElement && el.closest("input, textarea, select, [contenteditable=true], .monaco-editor")) return;
      const k = e.key.toLowerCase();
      const i = k >= "a" && k <= "d" ? k.charCodeAt(0) - 97 : k >= "1" && k <= "4" ? Number(k) - 1 : -1;
      if (i >= 0 && i < optionCount) onChange({ type: "mcq", choice: i });
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [question.type, revealed, optionCount, onChange]);

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        {showType && (
          <Badge variant="muted">
            {t(`type.${question.type}`)}
            {text.fallback && <UntranslatedBadge />}
          </Badge>
        )}
        <div className="text-[1.05rem] font-medium">
          <Inline text={qt.prompt} />
        </div>
      </div>

      {question.code && question.type !== "fill" && <StaticCode code={question.code} />}

      {question.type === "mcq" && answer.type === "mcq" && (
        <div className="grid gap-2">
          {(qt.options ?? []).map((opt, i) => {
            const chosen = answer.choice === i;
            const isRight = i === question.answer;
            return (
              <button
                key={i}
                disabled={revealed}
                onClick={() => onChange({ type: "mcq", choice: i })}
                className={cn(
                  "press flex items-center gap-3 rounded-[4px] px-4 py-3 text-left text-sm font-bold",
                  !chosen && !revealed && "bg-card",
                  !revealed && chosen && "bg-primary text-primary-foreground",
                  revealed && isRight && "flash-hit bg-success text-success-foreground",
                  revealed && chosen && !isRight && "shake bg-danger text-primary-foreground",
                  revealed && !isRight && !chosen && "bg-card opacity-60",
                )}
              >
                <span
                  className={cn(
                    "grid size-7 shrink-0 place-items-center rounded-[2px] border-2 border-current text-xs font-black",
                  )}
                >
                  {String.fromCharCode(65 + i)}
                </span>
                <span className="min-w-0 flex-1">
                  <Inline text={opt} />
                </span>
                {revealed && isRight && <CheckCircle2 className="size-4" />}
                {revealed && chosen && !isRight && <XCircle className="size-4" />}
              </button>
            );
          })}
        </div>
      )}

      {question.type === "output" && answer.type === "output" && (
        <textarea
          value={answer.text}
          disabled={revealed}
          onChange={(e) => onChange({ type: "output", text: e.target.value })}
          placeholder={t("typeOutput")}
          rows={Math.max(2, String(question.answer ?? "").split("\n").length + 1)}
          spellCheck={false}
          className={cn(
            "w-full resize-y rounded-[4px] border bg-code px-4 py-3 font-mono text-sm outline-none focus:border-primary focus:ring-1 focus:ring-primary",
            revealed && (correct ? "border-success" : "border-danger"),
          )}
        />
      )}

      {question.type === "fill" && answer.type === "fill" && <FillCode question={question} answer={answer} onChange={onChange} revealed={revealed} />}

      {question.type === "parsons" && answer.type === "parsons" && (
        <Parsons question={question} answer={answer} onChange={onChange} revealed={revealed} />
      )}

      {revealed && (
        <div className={cn("animate-rise rounded-[4px] border px-4 py-3", correct ? "border-success/40 bg-success-soft/60" : "border-danger/30 bg-danger-soft/60")}>
          <div className={cn("flex items-center gap-2 font-bold", correct ? "text-success" : "text-danger")}>
            {correct ? <CheckCircle2 className="size-4" /> : <XCircle className="size-4" />}
            {correct ? t("correct") : t("incorrect")}
          </div>
          {!correct && question.type !== "mcq" && (
            <div className="mt-2 text-sm">
              <span className="text-muted-foreground">{t("correctAnswer")}: </span>
              <pre className="mt-1 whitespace-pre-wrap rounded-[2px] bg-card/70 p-2 font-mono text-[13px]">{correctAnswerText(question, qt.options)}</pre>
            </div>
          )}
          {qt.explanation && (
            <div className="mt-2 text-sm">
              <Inline text={qt.explanation} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function FillCode({ question, answer, onChange, revealed }: { question: Question; answer: Extract<UserAnswer, { type: "fill" }>; onChange: (a: UserAnswer) => void; revealed: boolean }) {
  const t = useTranslations("quiz");
  const parts = (question.code ?? "").replace(/\n$/, "").split("___");
  const expected = (question.answer as (string | string[])[]) ?? [];
  return (
    <pre className="overflow-x-auto rounded-[4px] border bg-code p-4 font-mono text-[13.5px] leading-8">
      {parts.map((part, i) => (
        <span key={i}>
          {part}
          {i < parts.length - 1 && (
            <input
              aria-label={t("fillBlank", { n: i + 1 })}
              value={answer.blanks[i] ?? ""}
              disabled={revealed}
              onChange={(e) => {
                const blanks = [...answer.blanks];
                blanks[i] = e.target.value;
                onChange({ type: "fill", blanks });
              }}
              spellCheck={false}
              autoCapitalize="off"
              style={{ width: `${Math.max(4, (answer.blanks[i] ?? "").length + 2, String(Array.isArray(expected[i]) ? expected[i][0] : expected[i] ?? "").length + 1)}ch` }}
              className={cn(
                "mx-0.5 rounded-[2px] border-b-2 border-warning bg-warning-soft px-1 font-mono text-[13.5px] outline-none focus:border-primary focus:bg-accent",
                revealed && "border-transparent bg-muted",
              )}
            />
          )}
        </span>
      ))}
    </pre>
  );
}

function Parsons({ question, answer, onChange, revealed }: { question: Question; answer: Extract<UserAnswer, { type: "parsons" }>; onChange: (a: UserAnswer) => void; revealed: boolean }) {
  const t = useTranslations("quiz");
  const lines = question.lines ?? [];
  const shuffled = useMemo(() => {
    let s = shuffle(lines, seedOf(question.id));
    // Make sure the shuffled order is not already the answer.
    if (lines.length > 1 && JSON.stringify(s) === JSON.stringify(lines)) s = [...s.slice(1), s[0]];
    return s;
  }, [question.id]); // eslint-disable-line react-hooks/exhaustive-deps
  const remaining = shuffled.filter((l) => !answer.order.includes(l));

  return (
    <div className="grid gap-3 md:grid-cols-2">
      <div>
        <div className="mb-1.5 text-xs font-bold text-muted-foreground">{t("parsonsAvailable")}</div>
        <div className="min-h-24 space-y-1.5 rounded-[4px] border border-dashed p-2">
          {remaining.map((l) => (
            <button
              key={l}
              disabled={revealed}
              onClick={() => onChange({ type: "parsons", order: [...answer.order, l] })}
              className="flex w-full items-center gap-2 rounded-[4px] border bg-card px-3 py-2 text-left font-mono text-[13px] transition hover:border-primary/50 hover:bg-accent/40"
            >
              <GripVertical className="size-3.5 shrink-0 text-muted-foreground" />
              <span className="whitespace-pre">{l}</span>
            </button>
          ))}
        </div>
      </div>
      <div>
        <div className="mb-1.5 text-xs font-bold text-muted-foreground">{t("parsonsYours")}</div>
        <div className="min-h-24 space-y-1.5 rounded-[4px] border bg-code p-2">
          {answer.order.map((l, i) => {
            const right = revealed && lines[i] === l;
            return (
              <button
                key={l}
                disabled={revealed}
                onClick={() => onChange({ type: "parsons", order: answer.order.filter((x) => x !== l) })}
                className={cn(
                  "flex w-full items-center gap-2 rounded-[4px] border bg-card px-3 py-2 text-left font-mono text-[13px] animate-rise",
                  revealed && (right ? "border-success" : "border-danger"),
                )}
              >
                <span className="w-4 shrink-0 text-xs text-muted-foreground">{i + 1}</span>
                <span className="whitespace-pre">{l}</span>
              </button>
            );
          })}
        </div>
        {!revealed && <p className="mt-1.5 text-xs text-muted-foreground">{t("parsonsHint")}</p>}
      </div>
    </div>
  );
}
