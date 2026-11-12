"use client";

import { CheckCircle2, ChevronDown, Circle } from "lucide-react";
import { useTranslations } from "next-intl";
import { useMemo, useState } from "react";
import interviewJson from "@/generated/interview.json";
import { Markdown, StaticCode } from "@/components/markdown";
import { PageHeader } from "@/components/page-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { catalog } from "@/lib/content";
import { UntranslatedBadge, useLoc } from "@/lib/i18n";
import { useProgress } from "@/lib/progress";
import type { InterviewQuestion } from "@/lib/types";
import { cn } from "@/lib/utils";

const questions = (interviewJson as unknown as { questions: InterviewQuestion[] }).questions ?? [];

export default function InterviewPage() {
  const t = useTranslations("interview");
  const tc = useTranslations("common");
  const loc = useLoc();
  const practiced = useProgress((s) => s.practiced);
  const toggle = useProgress((s) => s.togglePracticed);
  const [topic, setTopic] = useState<string | null>(null);
  const [open, setOpen] = useState<Record<string, boolean>>({});
  const topics = useMemo(() => Array.from(new Set(questions.map((q) => q.topic))), []);
  const list = questions.filter((q) => !topic || q.topic === topic);
  const done = questions.filter((q) => practiced?.[q.id]).length;

  return (
    <div className="mx-auto max-w-3xl">
      <PageHeader title={t("title")} subtitle={t("subtitle")} />
      <div className="mb-6 flex items-center gap-3">
        <Progress value={questions.length ? done / questions.length : 0} tone="success" className="flex-1" />
        <span className="text-sm font-mono tabular-nums text-muted-foreground">
          {t("practiced")}: {done}/{questions.length}
        </span>
      </div>
      <div className="mb-6 flex flex-wrap gap-1.5">
        <TagButton active={!topic} onClick={() => setTopic(null)}>
          {tc("all")} · {questions.length}
        </TagButton>
        {topics.map((x) => (
          <TagButton key={x} active={topic === x} onClick={() => setTopic(topic === x ? null : x)}>
            {loc.t(catalog.topics[x]) ?? x} · {questions.filter((q) => q.topic === x).length}
          </TagButton>
        ))}
      </div>
      <div className="space-y-3">
        {list.map((q, i) => {
          const qa = loc.pick(q);
          const isOpen = Boolean(open[q.id]);
          const isPracticed = Boolean(practiced?.[q.id]);
          return (
            <div key={q.id} className="overflow-hidden rounded-lg border border-border bg-card">
              <button
                type="button"
                id={`accordion-trigger-${q.id}`}
                aria-expanded={isOpen}
                aria-controls={`accordion-panel-${q.id}`}
                onClick={() => setOpen((o) => ({ ...o, [q.id]: !o[q.id] }))}
                className="flex w-full items-start gap-3 p-5 text-left transition-colors hover:bg-accent/40 outline-none focus-visible:outline-2 focus-visible:outline-ring"
              >
                <span className="mt-0.5 font-mono text-xs tabular-nums text-muted-foreground">{i + 1}</span>
                <span className="min-w-0 flex-1">
                  <span className="mb-1.5 flex flex-wrap gap-1.5">
                    <Badge variant="muted">{loc.t(catalog.topics[q.topic]) ?? q.topic}</Badge>
                    <Badge variant="outline">{t(`level.${q.level}`)}</Badge>
                    {qa.fallback && <UntranslatedBadge />}
                  </span>
                  <span className="block font-medium">
                    <Markdown text={qa.value!.question} className="[&_p]:m-0" />
                  </span>
                </span>
                {isPracticed && <CheckCircle2 className="size-5 shrink-0 text-primary-ink" aria-hidden="true" />}
                <ChevronDown
                  className={cn(
                    "size-5 shrink-0 text-muted-foreground transition-transform motion-reduce:transition-none",
                    isOpen && "rotate-180",
                  )}
                  aria-hidden="true"
                />
              </button>
              {isOpen && (
                <div
                  id={`accordion-panel-${q.id}`}
                  role="region"
                  aria-labelledby={`accordion-trigger-${q.id}`}
                  className="space-y-3 border-t border-border bg-muted/20 p-5"
                >
                  {q.code && <StaticCode code={q.code} />}
                  <Markdown text={qa.value!.answer} />
                  <div>
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={() => toggle(q.id)}
                      className={cn(
                        isPracticed && "border-transparent bg-success-soft text-primary-ink hover:bg-success-soft/80",
                      )}
                    >
                      {isPracticed ? (
                        <CheckCircle2 className="size-4" aria-hidden="true" />
                      ) : (
                        <Circle className="size-4" aria-hidden="true" />
                      )}
                      {isPracticed ? t("practiced") : t("markPracticed")}
                    </Button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function TagButton({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      aria-pressed={active}
      onClick={onClick}
      className={cn(
        "hit h-9 rounded-full border px-3 text-sm transition-colors outline-none focus-visible:outline-2 focus-visible:outline-ring",
        active
          ? "border-primary bg-accent font-bold text-primary"
          : "border-border bg-card text-foreground hover:bg-accent",
      )}
    >
      {children}
    </button>
  );
}
