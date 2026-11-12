"use client";

import {
  BookA,
  Briefcase,
  ClipboardCheck,
  Flame,
  LayoutDashboard,
  Map,
  MessagesSquare,
  MoreHorizontal,
  Repeat,
  Settings,
  SquareTerminal,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { XpFigure } from "@/components/count-up";
import { LanguageSwitch, ThemeToggle } from "@/components/controls";
import { Logo } from "@/components/providers";
import { useProgress } from "@/lib/progress";
import { dueKeys, streak } from "@/lib/selectors";
import { cn } from "@/lib/utils";

const NAV = [
  { href: "/", key: "dashboard", icon: LayoutDashboard },
  { href: "/learn/", key: "learn", icon: Map },
  { href: "/review/", key: "review", icon: Repeat },
  { href: "/exams/", key: "exams", icon: ClipboardCheck },
  { href: "/playground/", key: "playground", icon: SquareTerminal },
  { href: "/glossary/", key: "glossary", icon: BookA },
  { href: "/interview/", key: "interview", icon: MessagesSquare },
  { href: "/portfolio/", key: "portfolio", icon: Briefcase },
  { href: "/settings/", key: "settings", icon: Settings },
] as const;

const MOBILE_MAIN = ["dashboard", "learn", "review", "exams"] as const;

function isActive(pathname: string, href: string) {
  if (href === "/") return pathname === "/";
  return pathname.startsWith(href.replace(/\/$/, "")) || (href === "/learn/" && pathname.startsWith("/lesson"));
}

function useDueCount() {
  return useProgress((s) => dueKeys(s).length);
}

export function AppShell({ children, fullBleed = false }: { children: React.ReactNode; fullBleed?: boolean }) {
  const t = useTranslations("nav");
  const pathname = usePathname();
  const due = useDueCount();
  const days = useProgress((s) => streak(s));
  const xp = useProgress((s) => s.xp);
  const [moreOpen, setMoreOpen] = useState(false);
  const full = fullBleed || pathname.startsWith("/lesson") || pathname.startsWith("/playground");

  return (
    <div className="flex min-h-dvh">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-2 focus:top-2 focus:z-50 focus:rounded-md focus:bg-card focus:px-3 focus:py-2 focus:outline-2 focus:outline-ring"
      >
        {t("skipToContent")}
      </a>

      {/* Desktop sidebar: Dose theme uses --muted ground */}
      <aside className="sticky top-0 hidden h-dvh w-64 shrink-0 flex-col border-r border-border bg-muted px-3 py-4 lg:flex">
        <Link href="/" className="mb-6 flex items-center gap-2.5 px-2" aria-label="PyAI Path">
          <Logo className="size-9" aria-hidden="true" />
          <span className="font-display text-xl font-bold leading-none tracking-tight">PyAI Path</span>
        </Link>
        <nav className="flex flex-1 flex-col gap-0.5">
          {NAV.map(({ href, key, icon: Icon }) => {
            const active = isActive(pathname, href);
            return (
              <Link
                key={key}
                href={href}
                aria-current={active ? "page" : undefined}
                className="group flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-accent hover:text-primary aria-[current=page]:bg-accent aria-[current=page]:font-bold aria-[current=page]:text-primary"
              >
                <Icon className="size-[18px]" aria-hidden="true" />
                <span className="flex-1">{t(key)}</span>
                {key === "review" && due > 0 && (
                  <span className="rounded-full bg-accent px-1.5 py-0.5 font-mono text-[11px] font-bold tabular-nums text-primary">
                    {due}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>
        <div className="well mt-auto flex items-end justify-between gap-2 px-3 py-3">
          <div>
            <Flame className={cn("mb-1 size-4", days > 0 ? "text-primary" : "text-muted-foreground")} aria-hidden="true" />
            <div className="figure font-mono text-3xl text-primary tabular-nums">{days}</div>
          </div>
          <div className="text-right">
            <XpFigure value={xp} className="figure font-mono text-3xl text-foreground tabular-nums" />
            <div className="mt-1 text-xs font-medium text-muted-foreground">XP</div>
          </div>
        </div>
        <div className="mt-3 flex items-center justify-between px-1">
          <LanguageSwitch />
          <ThemeToggle />
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        {/* Mobile top bar: solid background */}
        <header className="sticky top-0 z-30 flex h-14 items-center gap-2 border-b border-border bg-background px-4 lg:hidden">
          <Link href="/" className="flex items-center gap-2" aria-label="PyAI Path">
            <Logo className="size-7" aria-hidden="true" />
            <span className="font-display text-lg font-bold leading-none tracking-tight">PyAI Path</span>
          </Link>
          <div className="ml-auto flex items-center gap-2">
            <span className="flex items-center gap-1 font-mono text-sm font-medium tabular-nums">
              <Flame className={cn("size-4", days > 0 ? "text-primary" : "text-muted-foreground")} aria-hidden="true" />
              {days}
            </span>
            <LanguageSwitch />
            <ThemeToggle />
          </div>
        </header>

        <main id="main" className={cn("flex-1", full ? "" : "mx-auto w-full max-w-6xl px-4 pb-28 pt-6 sm:px-6 lg:px-10 lg:pb-12 lg:pt-10")}>
          {children}
        </main>

        {/* Mobile bottom nav: solid background */}
        <nav className="fixed inset-x-0 bottom-0 z-30 grid grid-cols-5 border-t border-border bg-background pb-[env(safe-area-inset-bottom)] lg:hidden">
          {NAV.filter((n) => (MOBILE_MAIN as readonly string[]).includes(n.key)).map(({ href, key, icon: Icon }) => {
            const active = isActive(pathname, href);
            return (
              <Link
                key={key}
                href={href}
                className={cn(
                  "relative flex flex-col items-center gap-0.5 py-2 text-[11px] font-medium transition-colors",
                  active ? "bg-accent font-bold text-primary" : "text-muted-foreground hover:text-foreground",
                )}
              >
                <Icon className="size-5" aria-hidden="true" />
                {t(key)}
                {key === "review" && due > 0 && <span className="absolute right-[28%] top-1.5 size-2 rounded-full bg-primary" aria-hidden="true" />}
              </Link>
            );
          })}
          <button
            type="button"
            onClick={() => setMoreOpen((v) => !v)}
            aria-label={t("more")}
            aria-expanded={moreOpen}
            className={cn(
              "flex flex-col items-center gap-0.5 py-2 text-[11px] font-medium transition-colors",
              moreOpen ? "bg-accent font-bold text-primary" : "text-muted-foreground hover:text-foreground",
            )}
          >
            <MoreHorizontal className="size-5" aria-hidden="true" />
            {t("more")}
          </button>
          {moreOpen && (
            <div className="absolute bottom-full right-2 mb-3 w-52 rounded-lg bg-popover p-1.5 shadow-[var(--shadow-lift)] animate-rise">
              {NAV.filter((n) => !(MOBILE_MAIN as readonly string[]).includes(n.key)).map(({ href, key, icon: Icon }) => (
                <Link
                  key={key}
                  href={href}
                  onClick={() => setMoreOpen(false)}
                  className="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-accent hover:text-primary"
                >
                  <Icon className="size-4" aria-hidden="true" />
                  {t(key)}
                </Link>
              ))}
            </div>
          )}
        </nav>
      </div>
    </div>
  );
}
