"use client";

import { ArrowRight, CheckCircle2, Download, FolderGit2, Lock } from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { StaticCode } from "@/components/markdown";
import { PageHeader } from "@/components/page-header";
import { PhaseIcon } from "@/components/phase-icon";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { catalog } from "@/lib/content";
import { Tx, useLoc } from "@/lib/i18n";
import { useProgress } from "@/lib/progress";
import { isLessonComplete, lessonParts } from "@/lib/selectors";

export default function PortfolioPage() {
  const t = useTranslations("portfolio");
  const tc = useTranslations("common");
  const loc = useLoc();
  const p = useProgress();
  const [openCode, setOpenCode] = useState<string | null>(null);
  const projects = catalog.phases.flatMap((ph) => ph.lessons.filter((l) => l.kind === "project").map((l) => ({ ...l, phase: ph })));

  const download = (lessonId: string, ids: string[]) => {
    const text = ids.map((id) => `# ===== ${id} =====\n${p.exercises[id]?.code ?? ""}`).join("\n\n");
    const url = URL.createObjectURL(new Blob([text], { type: "text/x-python" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = `${lessonId}.py`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <PageHeader title={t("title")} subtitle={t("subtitle")} />
      <h2 className="mb-3 text-base font-bold">{t("keyProjects")}</h2>
      <div className="grid gap-4 md:grid-cols-2">
        {projects.map((proj) => {
          const done = proj.ready && isLessonComplete(p, proj);
          const parts = proj.ready ? lessonParts(p, proj) : null;
          const ids = proj.exerciseIds ?? [];
          const completedAt = p.lessons[proj.id]?.completedAt;
          return (
            <Card key={proj.id} className={done ? "border-primary/40" : undefined}>
              <CardContent className="space-y-3 p-5">
                <div className="flex items-start gap-3">
                  <div className="grid size-10 shrink-0 place-items-center rounded-md bg-muted" aria-hidden="true">
                    <PhaseIcon name={proj.phase.icon} className="size-5" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="text-xs text-muted-foreground">{loc.t(proj.phase.title)}</div>
                    <h3 className="font-bold">
                      <Tx value={proj.title} />
                    </h3>
                  </div>
                  {done ? (
                    <Badge variant="success">
                      <CheckCircle2 className="size-3" aria-hidden="true" />
                      <span>{completedAt ? t("submitted", { date: completedAt.slice(0, 10) }) : tc("done")}</span>
                    </Badge>
                  ) : !proj.ready ? (
                    <Badge variant="outline">
                      <Lock className="size-3" aria-hidden="true" />
                      <span>{tc("comingSoon")}</span>
                    </Badge>
                  ) : null}
                </div>
                {parts && !done && (
                  <div className="space-y-2">
                    <Progress value={parts.fraction} />
                    <div className="flex items-center justify-between gap-3 text-sm">
                      <span className="text-muted-foreground">{t("notStarted")}</span>
                      <Button asChild variant="outline" size="sm">
                        <Link href={`/lesson/${proj.id}/`}>
                          {tc("continue")}
                          <ArrowRight className="size-4" aria-hidden="true" />
                        </Link>
                      </Button>
                    </div>
                  </div>
                )}
                {done && (
                  <div className="flex flex-wrap gap-2">
                    <Button type="button" variant="outline" size="sm" onClick={() => setOpenCode(openCode === proj.id ? null : proj.id)}>
                      <FolderGit2 className="size-4" aria-hidden="true" /> {openCode === proj.id ? t("hideCode") : t("viewCode")}
                    </Button>
                    <Button type="button" variant="ghost" size="sm" onClick={() => download(proj.id, ids)}>
                      <Download className="size-4" aria-hidden="true" /> {t("export")}
                    </Button>
                  </div>
                )}
                {openCode === proj.id && (
                  <div className="space-y-3">
                    {ids.map((id) => (
                      <StaticCode key={id} code={p.exercises[id]?.code ?? ""} />
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>

      <h2 className="mb-3 mt-10 text-base font-bold">{t("capstones")}</h2>
      <div className="grid gap-4 md:grid-cols-2">
        {catalog.capstones.map((c) => (
          <Card key={c.id} className="border-dashed bg-transparent">
            <CardContent className="flex items-center gap-3 p-5 text-muted-foreground">
              <Lock className="size-4" aria-hidden="true" />
              <Tx value={c.title} />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
