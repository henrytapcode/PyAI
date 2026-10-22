"use client";

import { ArrowRight, ClipboardCheck, Compass, GraduationCap, Lock } from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { PageHeader } from "@/components/page-header";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { catalog } from "@/lib/content";
import { Tx, useLoc } from "@/lib/i18n";
import { useProgress } from "@/lib/progress";
import type { ExamKind, ExamSummary } from "@/lib/types";
import { percent } from "@/lib/utils";

const GROUPS: { kind: ExamKind; key: "phaseTests" | "mocks" | "placement"; icon: typeof ClipboardCheck }[] = [
  { kind: "phase_test", key: "phaseTests", icon: ClipboardCheck },
  { kind: "mock", key: "mocks", icon: GraduationCap },
  { kind: "placement", key: "placement", icon: Compass },
];

export default function ExamsPage() {
  const t = useTranslations("exam");
  return (
    <div>
      <PageHeader title={t("title")} subtitle={t("subtitle")} />
      <div className="space-y-10">
        {GROUPS.map(({ kind, key, icon: Icon }) => {
          const exams = catalog.exams.filter((e) => e.kind === kind);
          return (
            <section key={kind}>
              <h2 className="mb-3 flex items-center gap-2 font-semibold">
                <Icon className="size-5 text-primary" /> {t(key)}
              </h2>
              <div className="grid gap-4 md:grid-cols-2">
                {exams.map((e) => (
                  <ExamCard key={e.id} exam={e} />
                ))}
                {kind === "mock" && (
                  <Card className="border-dashed bg-transparent">
                    <CardContent className="flex h-full items-center gap-3 p-5 text-sm text-muted-foreground">
                      <Lock className="size-4" /> {t("lockedMock")}
                    </CardContent>
                  </Card>
                )}
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}

function ExamCard({ exam }: { exam: ExamSummary }) {
  const t = useTranslations("exam");
  const loc = useLoc();
  const history = useProgress((s) => s.exams[exam.id]);
  const best = history?.length ? Math.max(...history.map((h) => h.score)) : undefined;
  const passed = history?.some((h) => h.passed);
  const href = exam.kind === "placement" ? "/placement/" : `/exam/${exam.id}/`;
  return (
    <Link href={href} className="group">
      <Card className="h-full transition hover:-translate-y-0.5 hover:shadow-md animate-rise">
        <CardContent className="flex h-full flex-col gap-3 p-5">
          <div className="flex items-start justify-between gap-3">
            <h3 className="font-semibold">
              <Tx value={exam.title} />
            </h3>
            {best !== undefined && <Badge variant={passed ? "success" : "muted"}>{t("best", { score: percent(best) })}</Badge>}
          </div>
          {exam.description && <p className="text-sm text-muted-foreground">{loc.t(exam.description)}</p>}
          <div className="mt-auto flex items-center justify-between text-xs text-muted-foreground">
            <span>{t("intro", { count: exam.questionCount, minutes: exam.duration_min, score: percent(exam.pass_score) })}</span>
            <ArrowRight className="size-4 transition group-hover:translate-x-0.5 group-hover:text-primary" />
          </div>
          <div className="text-xs text-muted-foreground">{t("attempts", { count: history?.length ?? 0 })}</div>
        </CardContent>
      </Card>
    </Link>
  );
}
