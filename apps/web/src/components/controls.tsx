"use client";

import { Monitor, Moon, Sun } from "lucide-react";
import { useTranslations } from "next-intl";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { Tooltip } from "@/components/ui/tooltip";
import { useProgress } from "@/lib/progress";
import type { Locale } from "@/lib/types";
import { cn } from "@/lib/utils";

export function LanguageSwitch({ className }: { className?: string }) {
  const locale = useProgress((s) => s.profile.locale);
  const setLocale = useProgress((s) => s.setLocale);
  const t = useTranslations("language");
  return (
    <div
      role="radiogroup"
      aria-label={t("switch")}
      className={cn("inline-flex rounded-md border border-border bg-muted p-0.5 text-xs font-medium", className)}
    >
      {(["vi", "en"] as Locale[]).map((l) => (
        <button
          key={l}
          role="radio"
          aria-checked={locale === l}
          title={t(l)}
          onClick={() => setLocale(l)}
          className={cn(
            "rounded-sm px-2.5 py-1 transition-colors outline-none focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-ring",
            locale === l ? "bg-card font-bold text-primary shadow-xs" : "text-muted-foreground hover:text-foreground",
          )}
        >
          {l.toUpperCase()}
        </button>
      ))}
    </div>
  );
}

export function ThemeToggle({ className }: { className?: string }) {
  const { theme, setTheme } = useTheme();
  const t = useTranslations("theme");
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  const order = ["light", "dark", "system"] as const;
  const current = (mounted ? theme : "system") as (typeof order)[number];
  const Icon = current === "light" ? Sun : current === "dark" ? Moon : Monitor;
  const next = order[(order.indexOf(current) + 1) % order.length];
  return (
    <Tooltip content={`${t("toggle")}: ${t(current)}`}>
      <button
        onClick={() => setTheme(next)}
        aria-label={t("toggle")}
        className={cn(
          "relative grid size-9 place-items-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-primary outline-none focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring after:absolute after:-inset-[4px] after:content-['']",
          className,
        )}
      >
        <Icon className="size-4" aria-hidden="true" />
      </button>
    </Tooltip>
  );
}

export function ThemeSelect() {
  const { theme, setTheme } = useTheme();
  const t = useTranslations("theme");
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  const items = [
    { id: "light", icon: Sun },
    { id: "dark", icon: Moon },
    { id: "system", icon: Monitor },
  ] as const;
  return (
    <div className="inline-flex rounded-md border border-border bg-muted p-0.5">
      {items.map(({ id, icon: Icon }) => (
        <button
          key={id}
          onClick={() => setTheme(id)}
          className={cn(
            "inline-flex items-center gap-1.5 rounded-sm px-3 py-1.5 text-sm font-medium transition-colors outline-none focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-ring",
            mounted && theme === id ? "bg-card font-bold text-primary shadow-xs" : "text-muted-foreground hover:text-foreground",
          )}
        >
          <Icon className="size-4" aria-hidden="true" />
          {t(id)}
        </button>
      ))}
    </div>
  );
}
