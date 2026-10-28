"use client";

import { NextIntlClientProvider } from "next-intl";
import { ThemeProvider } from "next-themes";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import en from "../../messages/en.json";
import vi from "../../messages/vi.json";
import { TooltipProvider } from "@/components/ui/tooltip";
import { VisualizerHost } from "@/components/visualizer";
import { useAuth } from "@/lib/auth";
import { useProgress } from "@/lib/progress";

// Compile-time parity check: vi.json must have exactly the same keys as en.json.
const viMessages: typeof en = vi;
const MESSAGES = { en, vi: viMessages } as const;

function useHydrated() {
  const [hydrated, setHydrated] = useState(false);
  useEffect(() => {
    const done = () => setHydrated(true);
    if (useProgress.persist.hasHydrated()) done();
    return useProgress.persist.onFinishHydration(done);
  }, []);
  return hydrated;
}

const OPEN_ROUTES = ["/onboarding", "/placement", "/login"];

export function Providers({ children }: { children: React.ReactNode }) {
  const hydrated = useHydrated();
  const locale = useProgress((s) => s.profile.locale);
  const onboarded = useProgress((s) => s.profile.onboarded);
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
    document.documentElement.lang = locale;
  }, [locale]);

  useEffect(() => {
    if (hydrated) useAuth.getState().init();
  }, [hydrated]);

  const needsOnboarding = hydrated && !onboarded && !OPEN_ROUTES.some((r) => pathname.startsWith(r));
  useEffect(() => {
    if (needsOnboarding) router.replace("/onboarding/");
  }, [needsOnboarding, router]);

  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
      <NextIntlClientProvider
        locale={locale}
        messages={MESSAGES[locale]}
        timeZone="Asia/Ho_Chi_Minh"
        onError={() => {}}
        getMessageFallback={({ namespace, key }) => [namespace, key].filter(Boolean).join(".")}
      >
        <TooltipProvider delayDuration={300}>
          {hydrated && !needsOnboarding ? children : <Splash />}
          <VisualizerHost />
        </TooltipProvider>
      </NextIntlClientProvider>
    </ThemeProvider>
  );
}

function Splash() {
  return (
    <div className="grid min-h-dvh place-items-center">
      <div className="flex items-center gap-3 text-muted-foreground">
        <Logo className="size-8 animate-pulse" />
      </div>
    </div>
  );
}

export function Logo({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden>
      <rect x="3" y="3" width="26" height="26" fill="var(--primary)" stroke="var(--edge)" strokeWidth="2" />
      <path d="M10 22V10h6a3.5 3.5 0 0 1 0 7H10" fill="none" stroke="var(--primary-foreground)" strokeWidth="2.6" strokeLinecap="square" />
      <rect x="20" y="19" width="4" height="4" fill="var(--primary-foreground)" />
    </svg>
  );
}
