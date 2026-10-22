"use client";

import { CheckCircle2, ChevronDown, Circle } from "lucide-react";
import { useTranslations } from "next-intl";
import { useMemo, useState } from "react";
import interviewJson from "@/generated/interview.json";
import { Markdown, StaticCode } from "@/components/markdown";
import { PageHeader } from "@/components/page-header";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
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
      <div className="mb-6 flex items-center gap-3 animate-rise">
        <Progress value={questions.length ? done / questions.length : 0} tone="success" className="flex-1" />
        <span className="text-sm tabular-nums text-muted-foreground">
          {t("practiced")}: {done}/{questions.length}
        </span>
      </div>
      <div className="mb-6 flex flex-wrap gap-1.5">
        <Chip active={!topic} onClick={() => setTopic(null)}>
          {tc("all")} · {questions.length}
        </Chip>
        {topics.map((x) => (
          <Chip key={x} active={topic === x} onClick={() => setTopic(topic === x ? null : x)}>
            {loc.t(catalog.topics[x]) ?? x} · {questions.filter((q) => q.topic === x).length}
          </Chip>
        ))}
      </div>
      <div className="space-y-3">
        {list.map((q, i) => {
          const qa = loc.pick(q);
          const isOpen = open[q.id];
          return (
            <Card key={q.id} className="animate-rise overflow-hidden">
              <CardContent className="p-0">
                <button onClick={() => setOpen((o) => ({ ...o, [q.id]: !o[q.id] }))} className="flex w-full items-start gap-3 p-5 text-left hover:bg-muted/40">
                  <span className="mt-0.5 text-xs tabular-nums text-muted-foreground">{i + 1}</span>
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
                  {practiced?.[q.id] && <CheckCircle2 className="size-5 shrink-0 text-success" />}
                  <ChevronDown className={cn("size-5 shrink-0 text-muted-foreground transition", isOpen && "rotate-180")} />
                </button>
                {isOpen && (
                  <div className="space-y-3 border-t bg-muted/20 p-5 animate-rise">
                    {q.code && <StaticCode code={q.code} />}
                    <Markdown text={qa.value!.answer} />
                    <button
                      onClick={() => toggle(q.id)}
                      className={cn("inline-flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-sm", practiced?.[q.id] ? "border-success/40 bg-success-soft text-success" : "hover:bg-muted")}
                    >
                      {practiced?.[q.id] ? <CheckCircle2 className="size-4" /> : <Circle className="size-4" />}
                      {practiced?.[q.id] ? t("practiced") : t("markPracticed")}
                    </button>
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

function Chip({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button onClick={onClick} className={cn("rounded-full border px-3 py-1 text-xs transition", active ? "border-primary bg-primary text-primary-foreground" : "bg-card hover:bg-muted")}>
      {children}
    </button>
  );
}
