"use client";

import { ArrowRight, Compass, Rocket } from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { LanguageSwitch, ThemeToggle } from "@/components/controls";
import { ExamRunner } from "@/components/exam-runner";
import { Logo } from "@/components/providers";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useProgress } from "@/lib/progress";
import type { Exam } from "@/lib/types";
import { percent } from "@/lib/utils";

export function PlacementView({ exam }: { exam: Exam }) {
  const t = useTranslations("placement");
  const tc = useTranslations("common");
  const finishOnboarding = useProgress((s) => s.finishOnboarding);
  const [outcome, setOutcome] = useState<boolean | null>(null);

  return (
    <div className="min-h-dvh">
      <header className="flex items-center gap-3 border-b px-4 py-3 sm:px-8">
        <Link href="/" className="flex items-center gap-2">
          <Logo className="size-7" />
          <span className="font-semibold">PyAI Path</span>
        </Link>
        <div className="ml-auto flex items-center gap-2">
          <LanguageSwitch />
          <ThemeToggle />
        </div>
      </header>
      <main className="mx-auto max-w-4xl px-4 py-10 sm:px-6">
        <div className="mb-8 text-center animate-rise">
          <Compass className="mx-auto size-9 text-primary" />
          <h1 className="mt-3 text-2xl font-semibold">{t("title")}</h1>
          <p className="mt-1 text-muted-foreground">{t("subtitle", { score: percent(exam.pass_score) })}</p>
        </div>
        {outcome !== null && (
          <Card className="mx-auto mb-6 max-w-3xl border-primary/30 bg-accent/40 animate-rise">
            <CardContent className="flex flex-wrap items-center gap-4 p-5">
              <Rocket className="size-6 text-primary" />
              <div className="flex-1">
                <div className="font-semibold">{outcome ? t("passedTitle") : t("failedTitle")}</div>
                <div className="text-sm text-muted-foreground">{outcome ? t("passedBody") : t("failedBody")}</div>
              </div>
              <Button asChild>
                <Link href="/">
                  {tc("continue")} <ArrowRight />
                </Link>
              </Button>
            </CardContent>
          </Card>
        )}
        <ExamRunner
          exam={exam}
          backHref="/"
          onFinished={(passed) => {
            finishOnboarding();
            setOutcome(passed);
          }}
        />
      </main>
    </div>
  );
}
