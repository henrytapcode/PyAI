"use client";

import { ArrowRight, CheckCircle2, Download, FolderGit2, Lock, Trophy } from "lucide-react";
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
import { capstones, catalog } from "@/lib/content";
import { Tx, useLoc } from "@/lib/i18n";
import { type ProgressData, useProgress } from "@/lib/progress";
import { isLessonComplete, lessonParts } from "@/lib/selectors";
import type { LessonSummary } from "@/lib/types";

interface ProjectCardProps {
  item: LessonSummary;
  label: string;
  icon: React.ReactNode;
  progress: ProgressData;
  isOpen: boolean;
  onToggleCode: () => void;
  onDownload: (lessonId: string, ids: string[]) => void;
}

function ProjectCard({ item, label, icon, progress, isOpen, onToggleCode, onDownload }: ProjectCardProps) {
  const t = useTranslations("portfolio");
  const tc = useTranslations("common");
  const done = item.ready && isLessonComplete(progress, item);
  const parts = item.ready ? lessonParts(progress, item) : null;
  const ids = item.exerciseIds ?? [];
  const completedAt = progress.lessons[item.id]?.completedAt;

  return (
    <Card className={done ? "border-primary/40" : undefined}>
      <CardContent className="space-y-3 p-5">
        <div className="flex items-start gap-3">
          <div className="grid size-10 shrink-0 place-items-center rounded-md bg-muted" aria-hidden="true">
            {icon}
          </div>
          <div className="min-w-0 flex-1">
            <div className="text-xs text-muted-foreground">{label}</div>
            <h3 className="font-bold">
              <Tx value={item.title} />
            </h3>
          </div>
          {done ? (
            <Badge variant="success">
              <CheckCircle2 className="size-3" aria-hidden="true" />
              <span>{completedAt ? t("submitted", { date: completedAt.slice(0, 10) }) : tc("done")}</span>
            </Badge>
          ) : !item.ready ? (
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
                <Link href={`/lesson/${item.id}/`}>
                  {tc("continue")}
                  <ArrowRight className="size-4" aria-hidden="true" />
                </Link>
              </Button>
            </div>
          </div>
        )}
        {done && (
          <div className="flex flex-wrap gap-2">
            <Button type="button" variant="outline" size="sm" onClick={onToggleCode}>
              <FolderGit2 className="size-4" aria-hidden="true" /> {isOpen ? t("hideCode") : t("viewCode")}
            </Button>
            <Button type="button" variant="ghost" size="sm" onClick={() => onDownload(item.id, ids)}>
              <Download className="size-4" aria-hidden="true" /> {t("export")}
            </Button>
          </div>
        )}
        {isOpen && (
          <div className="space-y-3">
            {ids.map((id) => (
              <StaticCode key={id} code={progress.exercises[id]?.code ?? ""} />
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default function PortfolioPage() {
  const t = useTranslations("portfolio");
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
        {projects.map((proj) => (
          <ProjectCard
            key={proj.id}
            item={proj}
            label={loc.t(proj.phase.title)}
            icon={<PhaseIcon name={proj.phase.icon} className="size-5" />}
            progress={p}
            isOpen={openCode === proj.id}
            onToggleCode={() => setOpenCode(openCode === proj.id ? null : proj.id)}
            onDownload={download}
          />
        ))}
      </div>

      <h2 className="mb-3 mt-10 text-base font-bold">{t("capstones")}</h2>
      <div className="grid gap-4 md:grid-cols-2">
        {capstones.map((c) =>
          c.ready ? (
            <ProjectCard
              key={c.id}
              item={c}
              label={t("capstoneLabel")}
              icon={<Trophy className="size-5" />}
              progress={p}
              isOpen={openCode === c.id}
              onToggleCode={() => setOpenCode(openCode === c.id ? null : c.id)}
              onDownload={download}
            />
          ) : (
            <Card key={c.id} className="border-dashed bg-transparent">
              <CardContent className="flex items-center gap-3 p-5 text-muted-foreground">
                <Lock className="size-4" aria-hidden="true" />
                <Tx value={c.title} />
              </CardContent>
            </Card>
          ),
        )}
      </div>
    </div>
  );
}
