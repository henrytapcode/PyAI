"use client";

import { Download, Info, LogIn, LogOut, RefreshCw, RotateCcw, Trash2, Upload } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { useRef, useState } from "react";
import { LanguageSwitch, ThemeSelect } from "@/components/controls";
import { PageHeader } from "@/components/page-header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { authEnabled, useAuth } from "@/lib/auth";
import { exportProgress, parseImport, useProgress } from "@/lib/progress";
import { cn, todayKey } from "@/lib/utils";

export default function SettingsPage() {
  const t = useTranslations("settings");
  const tl = useTranslations("language");
  const tt = useTranslations("theme");
  const router = useRouter();
  const p = useProgress();
  const fileRef = useRef<HTMLInputElement>(null);
  const [message, setMessage] = useState<{ ok: boolean; text: string } | null>(null);

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

        <Card>
          <CardHeader>
            <CardTitle>{t("appearance")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Row label={tl("switch")}>
              <LanguageSwitch />
            </Row>
            <Row label={tt("label")}>
              <ThemeSelect />
            </Row>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{t("learning")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Row label={t("track")}>
              <Segmented value={p.profile.track ?? "A"} options={[{ v: "A", l: t("trackA") }, { v: "B", l: t("trackB") }]} onChange={(v) => p.setTrack(v as "A" | "B")} />
            </Row>
            <Row label={t("dailyGoal")}>
              <Segmented value={String(p.profile.dailyGoal)} options={[20, 30, 50].map((g) => ({ v: String(g), l: `${g} XP` }))} onChange={(v) => p.setDailyGoal(Number(v))} />
            </Row>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>{t("data")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex flex-wrap gap-2">
              <Button variant="outline" onClick={doExport}>
                <Download /> {t("export")}
              </Button>
              <Button variant="outline" onClick={() => fileRef.current?.click()}>
                <Upload /> {t("import")}
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
            {message && <p className={cn("text-sm", message.ok ? "text-success" : "text-danger")}>{message.text}</p>}
            <div className="flex flex-wrap gap-2 border-t pt-4">
              <Button
                variant="ghost"
                onClick={() => {
                  useProgress.setState((s) => ({ profile: { ...s.profile, onboarded: false } }));
                  router.push("/onboarding/");
                }}
              >
                <RotateCcw /> {t("redoOnboarding")}
              </Button>
              <Button
                variant="ghost"
                className="text-danger hover:bg-danger-soft"
                onClick={() => {
                  if (window.confirm(t("resetConfirm"))) {
                    p.reset();
                    setMessage({ ok: true, text: t("resetDone") });
                  }
                }}
              >
                <Trash2 /> {t("reset")}
              </Button>
            </div>
            <p className="text-xs text-muted-foreground">{t("storage", { adapter: "localStorage" })}</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex gap-3 p-5 text-sm text-muted-foreground">
            <Info className="mt-0.5 size-4 shrink-0" />
            <div>
              <div className="mb-1 font-medium text-foreground">{t("about")}</div>
              {t("aboutBody")}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function AccountCard() {
  const t = useTranslations("auth");
  const user = useAuth((s) => s.user);
  const sync = useAuth((s) => s.sync);
  if (!authEnabled) return null;
  return (
    <Card>
      <CardHeader>
        <CardTitle>{t("account")}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {user ? (
          <>
            <p className="text-sm">{t("signedInAs", { email: user.email ?? "" })}</p>
            <p className="text-xs text-muted-foreground">{t(`sync.${sync}`)}</p>
            <div className="flex flex-wrap gap-2">
              <Button variant="outline" onClick={() => void useAuth.getState().syncNow()}>
                <RefreshCw /> {t("syncNow")}
              </Button>
              <Button variant="ghost" onClick={() => void useAuth.getState().signOut()}>
                <LogOut /> {t("signOut")}
              </Button>
            </div>
          </>
        ) : (
          <>
            <p className="text-sm text-muted-foreground">{t("guestBody")}</p>
            <Button asChild>
              <Link href="/login/">
                <LogIn /> {t("signIn")}
              </Link>
            </Button>
          </>
        )}
      </CardContent>
    </Card>
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

function Segmented({ value, options, onChange }: { value: string; options: { v: string; l: string }[]; onChange: (v: string) => void }) {
  return (
    <div className="inline-flex rounded-lg bg-muted p-0.5">
      {options.map((o) => (
        <button
          key={o.v}
          onClick={() => onChange(o.v)}
          className={cn("rounded-md px-3 py-1.5 text-sm", value === o.v ? "bg-card shadow-sm" : "text-muted-foreground hover:text-foreground")}
        >
          {o.l}
        </button>
      ))}
    </div>
  );
}
