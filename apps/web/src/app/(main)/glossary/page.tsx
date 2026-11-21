"use client";

import { Search } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useMemo, useState } from "react";
import glossaryJson from "@/generated/glossary.json";
import { PageHeader } from "@/components/page-header";
import { Badge } from "@/components/ui/badge";
import { catalog } from "@/lib/content";
import { UntranslatedBadge, useLoc } from "@/lib/i18n";
import type { GlossaryTerm } from "@/lib/types";
import { cn } from "@/lib/utils";

const terms = ((glossaryJson as unknown as { terms: GlossaryTerm[] }).terms ?? []).slice().sort((a, b) => a.term.localeCompare(b.term));

const strip = (s: string) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").toLowerCase();

export default function GlossaryPage() {
  const t = useTranslations("glossary");
  const tc = useTranslations("common");
  const loc = useLoc();
  const [query, setQuery] = useState("");
  const [tag, setTag] = useState<string | null>(null);
  const tags = useMemo(() => Array.from(new Set(terms.flatMap((x) => x.tags ?? []))).sort(), []);

  useEffect(() => {
    const applySearch = (search: string) => {
      const q = new URLSearchParams(search).get("q");
      if (q) {
        setTag(null);
        setQuery(q);
      }
    };
    applySearch(window.location.search);
    const onPopState = () => applySearch(window.location.search);
    const onDeepLink = (e: Event) => {
      const href = (e as CustomEvent<{ href?: string }>).detail?.href;
      if (href) {
        const url = new URL(href, window.location.origin);
        const pathname = url.pathname.replace(/\/+$/, "") || "/";
        const current = window.location.pathname.replace(/\/+$/, "") || "/";
        if (pathname !== "/glossary" && pathname !== current) return;
        applySearch(url.search);
      } else {
        applySearch(window.location.search);
      }
    };
    window.addEventListener("popstate", onPopState);
    window.addEventListener("pyai:deeplink", onDeepLink);
    return () => {
      window.removeEventListener("popstate", onPopState);
      window.removeEventListener("pyai:deeplink", onDeepLink);
    };
  }, []);

  const filtered = terms.filter((x) => {
    if (tag && !(x.tags ?? []).includes(tag)) return false;
    if (!query) return true;
    const q = strip(query);
    return [x.term, x.vi_term ?? "", x.en, x.vi ?? ""].some((f) => strip(f).includes(q));
  });

  return (
    <div>
      <PageHeader title={t("title")} subtitle={t("subtitle")} actions={<Badge variant="muted">{t("count", { count: terms.length })}</Badge>} />
      <div className="sticky top-14 z-10 -mx-4 mb-6 space-y-3 border-b border-border bg-background px-4 py-3 sm:-mx-6 sm:px-6 lg:top-0 lg:-mx-10 lg:px-10">
        <label className="flex h-10 items-center gap-2 rounded-md border border-border bg-card px-3 focus-within:outline-2 focus-within:outline-ring">
          <Search className="size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={t("placeholder")}
            aria-label={t("placeholder")}
            className="flex-1 bg-transparent text-sm outline-none placeholder:text-muted-foreground"
          />
        </label>
        <div className="flex flex-nowrap gap-1.5 overflow-x-auto pb-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden -mx-4 px-4 sm:mx-0 sm:px-0 sm:flex-wrap sm:overflow-visible sm:pb-0">
          <TagButton active={!tag} onClick={() => setTag(null)}>
            {tc("all")}
          </TagButton>
          {tags.map((x) => (
            <TagButton key={x} active={tag === x} onClick={() => setTag(tag === x ? null : x)}>
              {loc.t(catalog.topics[x]) ?? x}
            </TagButton>
          ))}
        </div>
      </div>
      {filtered.length === 0 ? (
        <p className="py-8 text-center text-sm text-muted-foreground">{t("empty")}</p>
      ) : (
        <div className="divide-y divide-border rounded-lg border border-border bg-card">
          {filtered.map((x) => {
            const def = loc.pick({ en: x.en, vi: x.vi });
            return (
              <div key={x.term} className="flex flex-col gap-2 p-4 sm:grid sm:grid-cols-[14rem_1fr] sm:gap-4 sm:p-5">
                <div className="flex flex-col gap-0.5">
                  <span className="font-mono text-sm font-bold">{x.term}</span>
                  {x.vi_term && x.vi_term !== x.term && (
                    <span className="text-sm text-muted-foreground">{x.vi_term}</span>
                  )}
                </div>
                <div className="space-y-2">
                  <p className="text-sm leading-relaxed">
                    {def.value}
                    {def.fallback && <UntranslatedBadge />}
                  </p>
                  {x.example && (
                    <pre className="overflow-x-auto rounded-md bg-code p-3 font-mono text-xs">{x.example}</pre>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function TagButton({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      type="button"
      aria-pressed={active}
      onClick={onClick}
      className={cn(
        "hit h-9 shrink-0 whitespace-nowrap rounded-full border px-3 text-sm transition-colors outline-none focus-visible:outline-2 focus-visible:outline-ring",
        active
          ? "border-primary bg-accent font-bold text-primary"
          : "border-border bg-card text-foreground hover:bg-accent",
      )}
    >
      {children}
    </button>
  );
}
