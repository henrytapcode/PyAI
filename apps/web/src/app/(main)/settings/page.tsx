"use client";

import { Download, Info, LogIn, LogOut, RefreshCw, RotateCcw, Trash2, Upload } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { useRef, useState } from "react";
import { LanguageSwitch, ThemeSelect } from "@/components/controls";
import { PageHeader } from "@/components/page-header";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogTitle,
} from "@/components/ui/dialog";
import { authEnabled, useAuth } from "@/lib/auth";
import { exportProgress, parseImport, useProgress } from "@/lib/progress";
import { cn, todayKey } from "@/lib/utils";

export default function SettingsPage() {
  const t = useTranslations("settings");
  const tc = useTranslations("common");
  const tl = useTranslations("language");
  const tt = useTranslations("theme");
  const router = useRouter();
  const p = useProgress();
  const fileRef = useRef<HTMLInputElement>(null);
  const [message, setMessage] = useState<{ ok: boolean; text: string } | null>(null);
  const [confirmReset, setConfirmReset] = useState(false);

  const doExport = () => {
    const url = URL.createObjectURL(new Blob([exportProgress()], { type: "application/json" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = `pyai-progress-${todayKey()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const doImport = async (file: File) => {
    try {
      p.importData(parseImport(await file.text()));
      setMessage({ ok: true, text: t("importOk") });
    } catch {
      setMessage({ ok: false, text: t("importFail") });
    }
  };

  return (
    <div className="mx-auto max-w-2xl">
      <PageHeader title={t("title")} subtitle={t("subtitle")} />
      <div className="space-y-6">
        <AccountCard />

        <section className="space-y-3">
          <div>
            <h2 className="text-base font-bold">{t("appearance")}</h2>
            <p className="text-sm text-muted-foreground">{t("appearanceDesc")}</p>
          </div>
          <Card>
            <CardContent className="space-y-4 p-5">
              <Row label={tl("switch")}>
                <LanguageSwitch />
              </Row>
              <Row label={tt("label")}>
                <ThemeSelect />
              </Row>
            </CardContent>
          </Card>
        </section>

        <section className="space-y-3">
          <div>
            <h2 className="text-base font-bold">{t("learning")}</h2>
            <p className="text-sm text-muted-foreground">{t("learningDesc")}</p>
          </div>
          <Card>
            <CardContent className="space-y-4 p-5">
              <Row label={t("track")}>
                <Segmented
                  label={t("track")}
                  value={p.profile.track ?? "A"}
                  options={[
                    { v: "A", l: t("trackA") },
                    { v: "B", l: t("trackB") },
                  ]}
                  onChange={(v) => p.setTrack(v as "A" | "B")}
                />
              </Row>
              <Row label={t("dailyGoal")}>
                <Segmented
                  label={t("dailyGoal")}
                  value={String(p.profile.dailyGoal)}
                  options={[20, 30, 50].map((g) => ({ v: String(g), l: `${g} XP` }))}
                  onChange={(v) => p.setDailyGoal(Number(v))}
                />
              </Row>
            </CardContent>
          </Card>
        </section>

        <section className="space-y-3">
          <div>
            <h2 className="text-base font-bold">{t("data")}</h2>
            <p className="text-sm text-muted-foreground">{t("dataDesc")}</p>
          </div>
          <Card>
            <CardContent className="space-y-3 p-5">
              <div className="flex flex-wrap gap-2">
                <Button type="button" variant="outline" onClick={doExport}>
                  <Download className="size-4" aria-hidden="true" /> {t("export")}
                </Button>
                <Button type="button" variant="outline" onClick={() => fileRef.current?.click()}>
                  <Upload className="size-4" aria-hidden="true" /> {t("import")}
                </Button>
                <input
                  ref={fileRef}
                  type="file"
                  accept="application/json,.json"
                  className="hidden"
                  onChange={(e) => {
                    const f = e.target.files?.[0];
                    if (f) void doImport(f);
                    e.target.value = "";
                  }}
                />
              </div>
              {message && message.text !== t("resetDone") && (
                <div
                  role="status"
                  className={cn(
                    "rounded-md px-3 py-2 text-sm",
                    message.ok ? "bg-success-soft text-primary-ink" : "bg-danger-soft text-danger",
                  )}
                >
                  {message.text}
                </div>
              )}
              <p className="text-xs text-muted-foreground">{t("storage", { adapter: "localStorage" })}</p>
            </CardContent>
          </Card>
        </section>

        <section className="space-y-3">
          <div>
            <h2 className="text-base font-bold text-danger">{t("dangerZone")}</h2>
            <p className="text-sm text-muted-foreground">{t("dangerZoneDesc")}</p>
          </div>
          <Card className="border-danger/30">
            <CardContent className="space-y-3 p-5">
              <div className="flex flex-wrap gap-2">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => {
                    useProgress.setState((s) => ({ profile: { ...s.profile, onboarded: false } }));
                    router.push("/onboarding/");
                  }}
                >
                  <RotateCcw className="size-4" aria-hidden="true" /> {t("redoOnboarding")}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  className="text-danger hover:bg-danger-soft hover:text-danger"
                  onClick={() => setConfirmReset(true)}
                >
                  <Trash2 className="size-4" aria-hidden="true" /> {t("reset")}
                </Button>
              </div>
              {message && message.text === t("resetDone") && (
                <div
                  role="status"
                  className={cn(
                    "rounded-md px-3 py-2 text-sm",
                    message.ok ? "bg-success-soft text-primary-ink" : "bg-danger-soft text-danger",
                  )}
                >
                  {message.text}
                </div>
              )}
            </CardContent>
          </Card>
        </section>

        <section className="space-y-3">
          <div>
            <h2 className="text-base font-bold">{t("about")}</h2>
          </div>
          <Card>
            <CardContent className="flex gap-3 p-5 text-sm text-muted-foreground">
              <Info className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
              <div>
                <p className="leading-relaxed">{t("aboutBody")}</p>
              </div>
            </CardContent>
          </Card>
        </section>
      </div>

      <Dialog open={confirmReset} onOpenChange={setConfirmReset}>
        <DialogContent>
          <DialogTitle>{t("reset")}</DialogTitle>
          <DialogDescription>{t("resetConfirm")}</DialogDescription>
          <div className="mt-4 flex flex-wrap justify-end gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => setConfirmReset(false)}
            >
              {tc("cancel")}
            </Button>
            <Button
              type="button"
              variant="danger"
              onClick={() => {
                p.reset();
                setMessage({ ok: true, text: t("resetDone") });
                setConfirmReset(false);
              }}
            >
              {tc("confirm")}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}

function AccountCard() {
  const t = useTranslations("auth");
  const user = useAuth((s) => s.user);
  const sync = useAuth((s) => s.sync);
  if (!authEnabled) return null;
  return (
    <section className="space-y-3">
      <div>
        <h2 className="text-base font-bold">{t("account")}</h2>
      </div>
      <Card>
        <CardContent className="space-y-3 p-5">
          {user ? (
            <>
              <p className="text-sm">{t("signedInAs", { email: user.email ?? "" })}</p>
              <p className="text-xs text-muted-foreground">{t(`sync.${sync}`)}</p>
              <div className="flex flex-wrap gap-2">
                <Button type="button" variant="outline" onClick={() => void useAuth.getState().syncNow()}>
                  <RefreshCw className="size-4" aria-hidden="true" /> {t("syncNow")}
                </Button>
                <Button type="button" variant="ghost" onClick={() => void useAuth.getState().signOut()}>
                  <LogOut className="size-4" aria-hidden="true" /> {t("signOut")}
                </Button>
              </div>
            </>
          ) : (
            <>
              <p className="text-sm text-muted-foreground">{t("guestBody")}</p>
              <Button asChild>
                <Link href="/login/">
                  <LogIn className="size-4" aria-hidden="true" /> {t("signIn")}
                </Link>
              </Button>
            </>
          )}
        </CardContent>
      </Card>
    </section>
  );
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3">
      <span className="text-sm font-medium">{label}</span>
      {children}
    </div>
  );
}

function Segmented({
  value,
  options,
  onChange,
  label,
}: {
  value: string;
  options: { v: string; l: string }[];
  onChange: (v: string) => void;
  label?: string;
}) {
  return (
    <div role="radiogroup" aria-label={label} className="inline-flex rounded-md bg-muted p-0.5">
      {options.map((o) => {
        const checked = value === o.v;
        return (
          <button
            key={o.v}
            type="button"
            role="radio"
            aria-checked={checked}
            onClick={() => onChange(o.v)}
            className={cn(
              "hit rounded-sm px-3 py-1.5 text-sm transition-colors outline-none focus-visible:outline-2 focus-visible:outline-ring",
              checked
                ? "bg-card font-bold text-primary"
                : "text-muted-foreground hover:text-foreground",
            )}
          >
            {o.l}
          </button>
        );
      })}
    </div>
  );
}
