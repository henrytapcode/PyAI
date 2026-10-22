"use client";

import { CheckCircle2, Download, FolderGit2, Lock } from "lucide-react";
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
      <h2 className="mb-3 font-semibold">{t("keyProjects")}</h2>
      <div className="grid gap-4 md:grid-cols-2">
        {projects.map((proj) => {
          const done = proj.ready && isLessonComplete(p, proj);
          const parts = proj.ready ? lessonParts(p, proj) : null;
          const ids = proj.exerciseIds ?? [];
          const completedAt = p.lessons[proj.id]?.completedAt;
          return (
            <Card key={proj.id} className={done ? "border-success/40" : ""}>
              <CardContent className="space-y-3 p-5">
                <div className="flex items-start gap-3">
                  <div className="grid size-10 shrink-0 place-items-center rounded-xl bg-muted">
                    <PhaseIcon name={proj.phase.icon} className="size-5" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="text-xs text-muted-foreground">{loc.t(proj.phase.title)}</div>
                    <h3 className="font-semibold">
                      <Tx value={proj.title} />
                    </h3>
                  </div>
                  {done ? (
                    <Badge variant="success">
                      <CheckCircle2 /> {completedAt ? t("submitted", { date: completedAt.slice(0, 10) }) : ""}
                    </Badge>
                  ) : !proj.ready ? (
                    <Badge variant="outline">
                      <Lock /> {tc("comingSoon")}
                    </Badge>
                  ) : null}
                </div>
                {parts && !done && (
                  <div className="space-y-1">
                    <Progress value={parts.fraction} />
                    <Link href={`/lesson/${proj.id}/`} className="text-sm text-primary hover:underline">
                      {t("notStarted")} → {tc("continue")}
                    </Link>
                  </div>
                )}
                {done && (
                  <div className="flex flex-wrap gap-2">
                    <Button variant="outline" size="sm" onClick={() => setOpenCode(openCode === proj.id ? null : proj.id)}>
                      <FolderGit2 /> {openCode === proj.id ? t("hideCode") : t("viewCode")}
                    </Button>
                    <Button variant="ghost" size="sm" onClick={() => download(proj.id, ids)}>
                      <Download /> {t("export")}
                    </Button>
                  </div>
                )}
                {openCode === proj.id && (
                  <div className="space-y-3 animate-rise">
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

      <h2 className="mb-3 mt-10 font-semibold">{t("capstones")}</h2>
      <div className="grid gap-4 md:grid-cols-2">
        {catalog.capstones.map((c) => (
          <Card key={c.id} className="border-dashed bg-transparent">
            <CardContent className="flex items-center gap-3 p-5 text-muted-foreground">
              <Lock className="size-4" />
              <Tx value={c.title} />
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
