"use client";

import { Search } from "lucide-react";
import { useTranslations } from "next-intl";
import { useMemo, useState } from "react";
import glossaryJson from "@/generated/glossary.json";
import { PageHeader } from "@/components/page-header";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
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

  const filtered = terms.filter((x) => {
    if (tag && !(x.tags ?? []).includes(tag)) return false;
    if (!query) return true;
    const q = strip(query);
    return [x.term, x.vi_term ?? "", x.en, x.vi ?? ""].some((f) => strip(f).includes(q));
  });

  return (
    <div>
      <PageHeader title={t("title")} subtitle={t("subtitle")} actions={<Badge variant="muted">{t("count", { count: terms.length })}</Badge>} />
      <div className="sticky top-14 z-10 -mx-4 mb-6 space-y-3 bg-background/90 px-4 py-2 backdrop-blur lg:top-0">
        <label className="flex items-center gap-2 rounded-xl border bg-card px-4 py-2.5 focus-within:ring-2 focus-within:ring-ring/40">
          <Search className="size-4 text-muted-foreground" />
          <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder={t("placeholder")} className="flex-1 bg-transparent outline-none" />
        </label>
        <div className="flex flex-wrap gap-1.5">
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
        <p className="text-muted-foreground">{t("empty")}</p>
      ) : (
        <div className="grid gap-3 md:grid-cols-2">
          {filtered.map((x) => {
            const def = loc.pick({ en: x.en, vi: x.vi });
            return (
              <Card key={x.term} className="animate-rise">
                <CardContent className="space-y-2 p-5">
                  <div className="flex flex-wrap items-baseline gap-2">
                    <h3 className="font-mono text-[15px] font-semibold">{x.term}</h3>
                    {x.vi_term && x.vi_term !== x.term && <span className="text-sm text-muted-foreground">· {x.vi_term}</span>}
                  </div>
                  <p className="text-sm leading-relaxed">
                    {def.value}
                    {def.fallback && <UntranslatedBadge />}
                  </p>
                  {x.example && <pre className="overflow-x-auto rounded-lg bg-code px-3 py-2 font-mono text-xs">{x.example}</pre>}
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}

function TagButton({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button onClick={onClick} className={cn("rounded-full border px-3 py-1 text-xs transition", active ? "border-primary bg-primary text-primary-foreground" : "bg-card hover:bg-muted")}>
      {children}
    </button>
  );
}
