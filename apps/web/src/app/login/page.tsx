"use client";

import { Mail } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { ThemeToggle } from "@/components/controls";
import { Logo } from "@/components/providers";
import { Button } from "@/components/ui/button";
import { authEnabled, useAuth } from "@/lib/auth";
import { cn } from "@/lib/utils";

const inputClass =
  "h-10 w-full rounded-[4px] border bg-card px-3 text-sm outline-none focus-visible:ring-2 focus-visible:ring-ring/50";

export default function LoginPage() {
  const t = useTranslations("auth");
  const router = useRouter();
  const user = useAuth((s) => s.user);
  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<{ ok: boolean; text: string } | null>(null);

  useEffect(() => {
    if (user) router.replace("/");
  }, [user, router]);

  const google = async () => {
    setBusy(true);
    const err = await useAuth.getState().signInWithGoogle();
    if (err) setMessage({ ok: false, text: err });
    setBusy(false);
  };

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setMessage(null);
    const { signInWithEmail, signUpWithEmail } = useAuth.getState();
    if (mode === "signin") {
      const err = await signInWithEmail(email, password);
      if (err) setMessage({ ok: false, text: err });
    } else {
      const res = await signUpWithEmail(email, password);
      if (res === "confirm") setMessage({ ok: true, text: t("checkEmail") });
      else if (res) setMessage({ ok: false, text: res });
    }
    setBusy(false);
  };

  return (
    <div className="relative grid min-h-dvh place-items-center overflow-hidden px-4 py-10">
      <div className="absolute right-4 top-4">
        <ThemeToggle />
      </div>
      <div className="relative w-full max-w-sm space-y-6">
        <div className="flex flex-col items-center gap-3 text-center">
          <Logo className="size-10" />
          <h1 className="text-2xl font-bold tracking-tight">{mode === "signin" ? t("signInTitle") : t("signUpTitle")}</h1>
          <p className="text-sm text-muted-foreground">{t("subtitle")}</p>
        </div>

        {!authEnabled ? (
          <p className="rounded-[4px] border bg-card p-4 text-sm text-muted-foreground">{t("notConfigured")}</p>
        ) : (
          <div className="space-y-4 rounded-[4px] border bg-card p-5">
            <Button variant="outline" className="w-full" disabled={busy} onClick={google}>
              <GoogleMark /> {t("google")}
            </Button>
            <div className="flex items-center gap-3 text-xs text-muted-foreground">
              <span className="h-px flex-1 bg-border" />
              {t("or")}
              <span className="h-px flex-1 bg-border" />
            </div>
            <form onSubmit={submit} className="space-y-3">
              <label className="block space-y-1 text-sm font-medium">
                {t("email")}
                <input
                  type="email"
                  required
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className={inputClass}
                />
              </label>
              <label className="block space-y-1 text-sm font-medium">
                {t("password")}
                <input
                  type="password"
                  required
                  minLength={8}
                  autoComplete={mode === "signin" ? "current-password" : "new-password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className={inputClass}
                />
              </label>
              {message && <p className={cn("text-sm", message.ok ? "text-success" : "text-danger")}>{message.text}</p>}
              <Button type="submit" className="w-full" disabled={busy}>
                <Mail /> {mode === "signin" ? t("signIn") : t("signUp")}
              </Button>
            </form>
            <button
              type="button"
              className="w-full text-center text-sm text-muted-foreground hover:text-foreground"
              onClick={() => {
                setMode(mode === "signin" ? "signup" : "signin");
                setMessage(null);
              }}
            >
              {mode === "signin" ? t("switchToSignUp") : t("switchToSignIn")}
            </button>
          </div>
        )}

        <div className="text-center">
          <Link href="/" className="text-sm text-muted-foreground underline-offset-4 hover:underline">
            {t("guest")}
          </Link>
        </div>
      </div>
    </div>
  );
}

function GoogleMark() {
  return (
    <svg viewBox="0 0 24 24" className="size-4" aria-hidden>
      <path fill="#4285F4" d="M23 12.3c0-.8-.1-1.5-.2-2.2H12v4.2h6.2a5.3 5.3 0 0 1-2.3 3.5v2.9h3.7c2.2-2 3.4-5 3.4-8.4Z" />
      <path fill="#34A853" d="M12 23.5c3.1 0 5.7-1 7.6-2.8l-3.7-2.9c-1 .7-2.3 1.1-3.9 1.1-3 0-5.5-2-6.4-4.7H1.8v3A11.5 11.5 0 0 0 12 23.5Z" />
      <path fill="#FBBC05" d="M5.6 14.2a6.9 6.9 0 0 1 0-4.4v-3H1.8a11.5 11.5 0 0 0 0 10.4l3.8-3Z" />
      <path fill="#EA4335" d="M12 5.4c1.7 0 3.2.6 4.4 1.7l3.3-3.3A11.5 11.5 0 0 0 1.8 6.8l3.8 3C6.5 7.4 9 5.4 12 5.4Z" />
    </svg>
  );
}
