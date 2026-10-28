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
    <div role="radiogroup" aria-label={t("switch")} className={cn("inline-flex rounded-[4px] border-2 border-border bg-muted p-0.5 text-xs font-bold", className)}>
      {(["vi", "en"] as Locale[]).map((l) => (
        <button
          key={l}
          role="radio"
          aria-checked={locale === l}
          title={t(l)}
          onClick={() => setLocale(l)}
          className={cn(
            "rounded-[2px] px-2.5 py-1",
            locale === l ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground",
          )}
        >
          {l}
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
        className={cn("row-cursor grid size-8 place-items-center rounded-[4px] text-muted-foreground hover:text-primary-foreground", className)}
      >
        <Icon className="size-4" />
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
    <div className="inline-flex rounded-[4px] border-2 border-border bg-muted p-0.5">
      {items.map(({ id, icon: Icon }) => (
        <button
          key={id}
          onClick={() => setTheme(id)}
          className={cn(
            "inline-flex items-center gap-1.5 rounded-[2px] px-3 py-1.5 text-sm font-bold",
            mounted && theme === id ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:text-foreground",
          )}
        >
          <Icon className="size-4" />
          {t(id)}
        </button>
      ))}
    </div>
  );
}
