"use client";

import { CheckCircle2, Circle, Eye, KeyRound, Lightbulb, Lock } from "lucide-react";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { Markdown, StaticCode } from "@/components/markdown";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogTitle } from "@/components/ui/dialog";
import { Tx, UntranslatedBadge, useLoc } from "@/lib/i18n";
import { useProgress } from "@/lib/progress";
import type { Exercise } from "@/lib/types";
import { cn } from "@/lib/utils";

export function ExercisePicker({ exercises, activeId, onPick }: { exercises: Exercise[]; activeId: string | null; onPick: (id: string) => void }) {
  const progress = useProgress((s) => s.exercises);
  return (
    <div className="flex flex-wrap gap-2">
      {exercises.map((ex, i) => {
        const passed = progress[ex.id]?.passed;
        const active = ex.id === activeId;
        return (
          <button
            key={ex.id}
            onClick={() => onPick(ex.id)}
            className={cn(
              "flex items-center gap-2 rounded-[4px] border px-3 py-2 text-left text-sm transition",
              active ? "border-primary bg-accent/60 ring-1 ring-primary" : "hover:bg-muted",
            )}
          >
            {passed ? <CheckCircle2 className="size-4 text-success" /> : <Circle className="size-4 text-muted-foreground" />}
            <span className="font-medium">{i + 1}.</span>
            <span className="max-w-[16rem] truncate">
              <Tx value={ex.title} />
            </span>
          </button>
        );
      })}
    </div>
  );
}

export function ExercisePanel({ exercise, onLoadCode }: { exercise: Exercise; onLoadCode: (code: string) => void }) {
  const t = useTranslations("exercise");
  const tc = useTranslations("common");
  const loc = useLoc();
  const state = useProgress((s) => s.exercises[exercise.id]);
  const showHint = useProgress((s) => s.showHint);
  const viewSolution = useProgress((s) => s.viewSolution);
  const [confirmOpen, setConfirmOpen] = useState(false);

  const attempts = state?.attempts ?? 0;
  const hintsShown = state?.hintsShown ?? 0;
  const hints = loc.pick(exercise.hints);
  const prompt = loc.pick(exercise.prompt);
  const solutionUnlocked = !!state?.passed || attempts >= exercise.solution_unlock_attempts || hintsShown >= 3;
  const solutionVisible = !!state?.solutionViewed || !!state?.passed;

  return (
    <div className="space-y-6">
      <div>
        <div className="mb-2 flex flex-wrap items-center gap-2">
          <Badge>{t(`kind.${exercise.kind}`)}</Badge>
          <span className="flex items-center gap-1 text-xs text-muted-foreground" title={t("difficulty")}>
            {[1, 2, 3].map((d) => (
              <span key={d} className={cn("size-1.5 rounded-[2px]", d <= exercise.difficulty ? "bg-primary" : "bg-muted-foreground/25")} />
            ))}
          </span>
          <span className="text-xs text-muted-foreground">· {t("attempts", { count: attempts })}</span>
          {state?.passed && (
            <Badge variant="success">
              <CheckCircle2 /> {t("passed")}
            </Badge>
          )}
        </div>
        <h2 className="text-xl font-bold">
          <Tx value={exercise.title} />
        </h2>
      </div>

      {prompt.fallback && <UntranslatedBadge />}
      <Markdown text={prompt.value ?? ""} />

      {/* 3-tier hints */}
      <section className="space-y-2">
        <h3 className="flex items-center gap-2 text-sm font-bold">
          <Lightbulb className="size-4 text-warning" />
          {t("hints")}
        </h3>
        {(hints.value ?? []).slice(0, hintsShown).map((h, i) => (
          <div key={i} className="animate-rise rounded-[4px] border border-warning/30 bg-warning-soft/50 px-4 py-3 text-sm">
            <div className="mb-1 text-xs font-bold text-warning">{t("hintLevel", { n: i + 1 })}</div>
            <Markdown text={h} className="[&_p]:m-0" />
          </div>
        ))}
        {hintsShown < 3 ? (
          <Button variant="outline" size="sm" onClick={() => showHint(exercise.id)}>
            <Lightbulb />
            {t("showHint", { n: hintsShown + 1 })}
          </Button>
        ) : (
          <p className="text-xs text-muted-foreground">{t("noMoreHints")}</p>
        )}
      </section>

      {/* Solution, hidden until enough attempts */}
      <section className="space-y-2">
        <h3 className="flex items-center gap-2 text-sm font-bold">
          <KeyRound className="size-4 text-muted-foreground" />
          {t("solution")}
        </h3>
        {solutionVisible ? (
          <div className="space-y-2 animate-rise">
            <StaticCode code={exercise.solution} />
            <Button variant="outline" size="sm" onClick={() => onLoadCode(exercise.solution)}>
              {t("loadSolution")}
            </Button>
            {exercise.alternatives?.length > 0 && (
              <div className="space-y-3 pt-2">
                <h4 className="text-sm font-bold">{t("otherApproaches")}</h4>
                {exercise.alternatives.map((alt) => (
                  <div key={alt.name} className="space-y-1">
                    <p className="text-sm font-medium">{loc.t(alt.title)}</p>
                    <Markdown text={loc.t(alt.explain) ?? ""} />
                    <StaticCode code={alt.code} />
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : solutionUnlocked ? (
          <Button variant="outline" size="sm" onClick={() => setConfirmOpen(true)}>
            <Eye />
            {t("showSolution")}
          </Button>
        ) : (
          <p className="flex items-center gap-2 text-xs text-muted-foreground">
            <Lock className="size-3.5" />
            {t("solutionLocked", { count: exercise.solution_unlock_attempts })}
          </p>
        )}
      </section>

      <Dialog open={confirmOpen} onOpenChange={setConfirmOpen}>
        <DialogContent>
          <DialogTitle>{t("showSolution")}</DialogTitle>
          <DialogDescription>{t("solutionWarning")}</DialogDescription>
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => setConfirmOpen(false)}>
              {tc("retry")}
            </Button>
            <Button
              onClick={() => {
                viewSolution(exercise.id);
                setConfirmOpen(false);
              }}
            >
              {t("showSolution")}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
