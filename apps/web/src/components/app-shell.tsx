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
      <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:left-2 focus:top-2 focus:z-50 focus:rounded-md focus:bg-card focus:px-3 focus:py-2">
        {t("skipToContent")}
      </a>

      {/* Desktop sidebar */}
      <aside className="sticky top-0 hidden h-dvh w-60 shrink-0 flex-col border-r bg-card/50 px-3 py-4 lg:flex">
        <Link href="/" className="mb-6 flex items-center gap-2.5 px-2">
          <Logo className="size-8" />
          <span className="font-semibold tracking-tight">PyAI Path</span>
        </Link>
        <nav className="flex flex-1 flex-col gap-0.5">
          {NAV.map(({ href, key, icon: Icon }) => {
            const active = isActive(pathname, href);
            return (
              <Link
                key={key}
                href={href}
                className={cn(
                  "group flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
                  active ? "bg-accent font-medium text-accent-foreground" : "text-muted-foreground hover:bg-muted hover:text-foreground",
                )}
              >
                <Icon className="size-[18px]" />
                <span className="flex-1">{t(key)}</span>
                {key === "review" && due > 0 && (
                  <span className="rounded-full bg-primary px-1.5 py-0.5 text-[10px] font-semibold text-primary-foreground">{due}</span>
                )}
              </Link>
            );
          })}
        </nav>
        <div className="mt-4 flex items-center gap-3 rounded-xl border bg-card px-3 py-2.5 text-sm">
          <Flame className={cn("size-5", days > 0 ? "text-warning" : "text-muted-foreground")} />
          <span className="font-semibold">{days}</span>
          <span className="ml-auto text-xs text-muted-foreground">{xp} XP</span>
        </div>
        <div className="mt-3 flex items-center justify-between px-1">
          <LanguageSwitch />
          <ThemeToggle />
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        {/* Mobile top bar */}
        <header className="sticky top-0 z-30 flex h-14 items-center gap-2 border-b bg-background/85 px-4 backdrop-blur lg:hidden">
          <Link href="/" className="flex items-center gap-2">
            <Logo className="size-7" />
            <span className="font-semibold tracking-tight">PyAI Path</span>
          </Link>
          <div className="ml-auto flex items-center gap-2">
            <span className="flex items-center gap-1 text-sm font-semibold">
              <Flame className={cn("size-4", days > 0 ? "text-warning" : "text-muted-foreground")} />
              {days}
            </span>
            <LanguageSwitch />
            <ThemeToggle />
          </div>
        </header>

        <main id="main" className={cn("flex-1", full ? "" : "mx-auto w-full max-w-6xl px-4 pb-28 pt-6 sm:px-6 lg:px-10 lg:pb-12 lg:pt-10")}>
          {children}
        </main>

        {/* Mobile bottom nav */}
        <nav className="fixed inset-x-0 bottom-0 z-30 grid grid-cols-5 border-t bg-background/95 pb-[env(safe-area-inset-bottom)] backdrop-blur lg:hidden">
          {NAV.filter((n) => (MOBILE_MAIN as readonly string[]).includes(n.key)).map(({ href, key, icon: Icon }) => {
            const active = isActive(pathname, href);
            return (
              <Link key={key} href={href} className={cn("relative flex flex-col items-center gap-0.5 py-2 text-[11px]", active ? "text-primary" : "text-muted-foreground")}>
                <Icon className="size-5" />
                {t(key)}
                {key === "review" && due > 0 && <span className="absolute right-[28%] top-1.5 size-2 rounded-full bg-primary" />}
              </Link>
            );
          })}
          <button onClick={() => setMoreOpen((v) => !v)} className={cn("flex flex-col items-center gap-0.5 py-2 text-[11px]", moreOpen ? "text-primary" : "text-muted-foreground")}>
            <MoreHorizontal className="size-5" />
            {t("more")}
          </button>
          {moreOpen && (
            <div className="absolute bottom-full right-2 mb-2 w-52 rounded-xl border bg-popover p-1.5 shadow-xl animate-rise">
              {NAV.filter((n) => !(MOBILE_MAIN as readonly string[]).includes(n.key)).map(({ href, key, icon: Icon }) => (
                <Link key={key} href={href} onClick={() => setMoreOpen(false)} className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm hover:bg-muted">
                  <Icon className="size-4 text-muted-foreground" />
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
