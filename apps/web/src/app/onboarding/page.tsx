"use client";

import { ArrowRight, Check, Compass, Sprout } from "lucide-react";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { ThemeToggle } from "@/components/controls";
import { Logo } from "@/components/providers";
import { Button } from "@/components/ui/button";
import { useProgress } from "@/lib/progress";
import type { Locale } from "@/lib/types";
import { cn } from "@/lib/utils";

export default function OnboardingPage() {
  const t = useTranslations("onboarding");
  const tl = useTranslations("language");
  const tc = useTranslations("common");
  const router = useRouter();
  const locale = useProgress((s) => s.profile.locale);
  const track = useProgress((s) => s.profile.track);
  const goal = useProgress((s) => s.profile.dailyGoal);
  const { setLocale, setTrack, setDailyGoal, finishOnboarding } = useProgress.getState();
  const [step, setStep] = useState(0);
  const total = 3;

  const done = () => {
    if (track === "B") {
      finishOnboarding();
      router.push("/placement/");
    } else {
      finishOnboarding();
      router.push("/");
    }
  };

  return (
    <div className="relative grid min-h-dvh place-items-center overflow-hidden px-4 py-10">
      <div className="absolute right-4 top-4">
        <ThemeToggle />
      </div>
      <div className="relative w-full max-w-xl">
        <div className="mb-8 flex flex-col items-center text-center animate-rise">
          <Logo className="size-14" />
          <h1 className="mt-5 text-3xl font-bold tracking-tight">{t("welcome")}</h1>
          <p className="mt-3 max-w-md text-muted-foreground">{t("intro")}</p>
        </div>

        <div className="rounded-[4px] border bg-card p-6 sm:p-8">
          <div className="mb-6 flex items-center gap-2">
            {Array.from({ length: total }, (_, i) => (
              <div key={i} className={cn("h-1.5 flex-1 rounded-[2px] transition-colors", i <= step ? "bg-primary" : "bg-muted")} />
            ))}
          </div>
          <div className="mb-1 text-xs text-muted-foreground">{t("step", { n: step + 1, total })}</div>

          {step === 0 && (
            <div key="lang" className="animate-rise">
              <h2 className="mb-4 text-lg font-bold">{t("chooseLanguage")}</h2>
              <div className="grid gap-3 sm:grid-cols-2">
                {(["vi", "en"] as Locale[]).map((l) => (
                  <Choice key={l} active={locale === l} onClick={() => setLocale(l)} title={tl(l)} code={l.toUpperCase()} />
                ))}
              </div>
            </div>
          )}

          {step === 1 && (
            <div key="track" className="animate-rise">
              <h2 className="mb-4 text-lg font-bold">{t("chooseTrack")}</h2>
              <div className="grid gap-3">
                <Choice active={track === "A"} onClick={() => setTrack("A")} title={t("trackA")} desc={t("trackADesc")} icon={<Sprout className="size-5" />} />
                <Choice active={track === "B"} onClick={() => setTrack("B")} title={t("trackB")} desc={t("trackBDesc")} icon={<Compass className="size-5" />} />
              </div>
            </div>
          )}

          {step === 2 && (
            <div key="goal" className="animate-rise">
              <h2 className="mb-4 text-lg font-bold">{t("goal")}</h2>
              <div className="grid gap-3">
                {[
                  { v: 20, label: t("goalCasual") },
                  { v: 30, label: t("goalRegular") },
                  { v: 50, label: t("goalSerious") },
                ].map((g) => (
                  <Choice key={g.v} active={goal === g.v} onClick={() => setDailyGoal(g.v)} title={g.label} />
                ))}
              </div>
            </div>
          )}

          <div className="mt-8 flex items-center justify-between">
            <Button variant="ghost" onClick={() => setStep(step - 1)} disabled={step === 0}>
              {tc("back")}
            </Button>
            {step < total - 1 ? (
              <Button onClick={() => setStep(step + 1)} disabled={step === 1 && !track}>
                {tc("next")} <ArrowRight />
              </Button>
            ) : (
              <Button size="lg" onClick={done}>
                {track === "B" ? t("toPlacement") : t("letsGo")} <ArrowRight />
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function Choice({ active, onClick, title, desc, code, icon }: { active: boolean; onClick: () => void; title: string; desc?: string; code?: string; icon?: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "flex items-start gap-3 rounded-[4px] border p-4 text-left transition",
        active ? "border-primary bg-accent/50 ring-1 ring-primary" : "hover:border-primary/40 hover:bg-muted/50",
      )}
    >
      {code && <span className="grid size-9 shrink-0 place-items-center rounded-[4px] bg-muted font-mono text-sm font-bold text-primary">{code}</span>}
      {icon && <span className="mt-0.5 grid size-9 shrink-0 place-items-center rounded-[4px] bg-muted text-primary">{icon}</span>}
      <span className="min-w-0 flex-1">
        <span className="block font-medium">{title}</span>
        {desc && <span className="mt-1 block text-sm text-muted-foreground">{desc}</span>}
      </span>
      <span className={cn("grid size-5 shrink-0 place-items-center rounded-[2px] border", active && "border-primary bg-primary text-primary-foreground")}>
        {active && <Check className="size-3" />}
      </span>
    </button>
  );
}
