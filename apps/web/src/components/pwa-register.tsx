"use client";

import { RefreshCw, WifiOff, X } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";

const BASE = process.env.NEXT_PUBLIC_BASE_PATH || "";

export function PwaRegister() {
  const t = useTranslations("pwa");
  const [offline, setOffline] = useState(false);
  const [offlineDismissed, setOfflineDismissed] = useState(false);
  const [waitingWorker, setWaitingWorker] = useState<ServiceWorker | null>(null);
  const reloadingRef = useRef(false);

  useEffect(() => {
    const syncOnline = () => {
      const isOffline = !navigator.onLine;
      setOffline(isOffline);
      if (!isOffline) setOfflineDismissed(false);
    };
    syncOnline();
    window.addEventListener("online", syncOnline);
    window.addEventListener("offline", syncOnline);
    return () => {
      window.removeEventListener("online", syncOnline);
      window.removeEventListener("offline", syncOnline);
    };
  }, []);

  useEffect(() => {
    if (process.env.NODE_ENV !== "production") return;
    if (!("serviceWorker" in navigator)) return;

    let cancelled = false;

    const onControllerChange = () => {
      if (reloadingRef.current) return;
      reloadingRef.current = true;
      window.location.reload();
    };
    navigator.serviceWorker.addEventListener("controllerchange", onControllerChange);

    const register = async () => {
      try {
        const reg = await navigator.serviceWorker.register(`${BASE}/sw.js`, {
          scope: `${BASE}/`,
        });
        if (cancelled) return;

        if (reg.waiting && navigator.serviceWorker.controller) {
          setWaitingWorker(reg.waiting);
        }

        reg.addEventListener("updatefound", () => {
          const installing = reg.installing;
          if (!installing) return;
          installing.addEventListener("statechange", () => {
            if (cancelled) return;
            if (installing.state === "installed" && navigator.serviceWorker.controller) {
              setWaitingWorker(installing);
            }
          });
        });
      } catch {
        // Ignore registration errors in restricted or private browsing contexts.
      }
    };

    register();

    return () => {
      cancelled = true;
      navigator.serviceWorker.removeEventListener("controllerchange", onControllerChange);
    };
  }, []);

  const showOffline = offline && !offlineDismissed;
  const showUpdate = waitingWorker !== null;

  if (!showOffline && !showUpdate) return null;

  return (
    <div
      role="status"
      aria-live="polite"
      className="fixed bottom-[calc(4.5rem+env(safe-area-inset-bottom))] right-4 z-40 flex max-w-[calc(100vw-2rem)] sm:max-w-sm flex-col gap-2 lg:bottom-4"
    >
      {showUpdate && (
        <div className="animate-rise flex items-center gap-3 rounded-lg border border-border bg-card px-3.5 py-2.5 text-sm text-foreground shadow-[var(--shadow-lift)]">
          <RefreshCw className="size-4 shrink-0 text-primary" aria-hidden="true" />
          <span className="flex-1 min-w-0 break-words font-medium">{t("updateReady")}</span>
          <button
            type="button"
            onClick={() => waitingWorker.postMessage({ type: "SKIP_WAITING" })}
            className="hit shrink-0 rounded-md bg-primary px-3 py-1.5 text-xs font-bold text-primary-foreground transition-[transform,background-color] duration-[120ms] hover:bg-primary/90 active:scale-[0.97] motion-reduce:transition-none motion-reduce:active:scale-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
          >
            {t("reload")}
          </button>
          <button
            type="button"
            onClick={() => setWaitingWorker(null)}
            aria-label={t("dismiss")}
            className="hit grid size-7 shrink-0 place-items-center rounded-md text-muted-foreground transition-[transform,background-color,color] duration-[120ms] hover:bg-accent hover:text-foreground active:scale-[0.97] motion-reduce:transition-none motion-reduce:active:scale-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        </div>
      )}

      {showOffline && (
        <div className="animate-rise flex items-start gap-2.5 rounded-lg border border-border bg-warning-soft px-3.5 py-2.5 text-xs text-warning-ink shadow-[var(--shadow-lift)]">
          <WifiOff className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
          <div className="flex-1 min-w-0 break-words">
            <div className="font-bold">{t("offlineTitle")}</div>
            <p className="mt-0.5 leading-snug opacity-90">{t("offlineBody")}</p>
          </div>
          <button
            type="button"
            onClick={() => setOfflineDismissed(true)}
            aria-label={t("dismiss")}
            className="hit grid size-7 shrink-0 place-items-center rounded-md text-warning-ink transition-[transform,background-color] duration-[120ms] hover:bg-card/60 active:scale-[0.97] motion-reduce:transition-none motion-reduce:active:scale-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        </div>
      )}
    </div>
  );
}
