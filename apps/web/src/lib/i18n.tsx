"use client";

import { useLocale } from "next-intl";
import { Languages } from "lucide-react";
import { useTranslations } from "next-intl";
import type { I18n, Locale } from "./types";

/** Pick the current locale's value from a bilingual object, falling back to EN. */
export function pick<T>(value: I18n<T> | Partial<Record<Locale, T>> | undefined, locale: Locale): { value: T | undefined; fallback: boolean } {
  if (!value) return { value: undefined, fallback: false };
  const own = value[locale];
  if (own !== undefined && own !== null) return { value: own, fallback: false };
  return { value: value.en, fallback: locale !== "en" };
}

export function useLoc() {
  const locale = useLocale() as Locale;
  return {
    locale,
    /** Plain string/array in the current locale (EN fallback, no badge). */
    t: <T,>(value: I18n<T> | Partial<Record<Locale, T>> | undefined): T => pick(value, locale).value as T,
    pick: <T,>(value: I18n<T> | Partial<Record<Locale, T>> | undefined) => pick(value, locale),
  };
}

/** Small "not translated" marker shown next to content that fell back to English. */
export function UntranslatedBadge() {
  const t = useTranslations("common");
  return (
    <span
      title={t("notTranslated")}
      className="ml-1.5 inline-flex items-center gap-1 rounded-[2px] bg-warning-soft px-1.5 py-0.5 align-middle text-[10px] font-medium text-warning"
    >
      <Languages className="size-3" />
      EN
    </span>
  );
}

/** Render a bilingual string with the fallback badge when needed. */
export function Tx({ value }: { value: I18n | Partial<Record<Locale, string>> | undefined }) {
  const locale = useLocale() as Locale;
  const res = pick(value, locale);
  return (
    <>
      {res.value}
      {res.fallback && <UntranslatedBadge />}
    </>
  );
}
