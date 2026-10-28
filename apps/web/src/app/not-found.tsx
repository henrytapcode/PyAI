"use client";

import Link from "next/link";
import { useTranslations } from "next-intl";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  const t = useTranslations("errors");
  return (
    <div className="grid min-h-dvh place-items-center p-6 text-center">
      <div>
        <div className="font-mono text-6xl font-bold text-primary">404</div>
        <h1 className="mt-3 text-xl font-bold">{t("notFound")}</h1>
        <Button asChild className="mt-6">
          <Link href="/">{t("goHome")}</Link>
        </Button>
      </div>
    </div>
  );
}
