"use client";

import { ClipboardCheck, Compass, GraduationCap, Lock } from "lucide-react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { PageHeader } from "@/components/page-header";
import { Badge } from "@/components/ui/badge";
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
              <h2 className="mb-3 flex items-center gap-2 text-lg font-bold">
                <Icon className="size-5 text-primary" aria-hidden="true" />
                {t(key)}
              </h2>
              <div className="overflow-x-auto rounded-lg border border-border bg-card">
                <table className="w-full min-w-[640px] table-fixed text-sm">
                  <colgroup>
                    <col className="w-auto" />
                    <col className="w-28" />
                    <col className="w-28" />
                    <col className="w-28" />
                    <col className="w-28" />
                    <col className="w-28" />
                  </colgroup>
                  <thead>
                    <tr className="border-b border-border bg-muted">
                      <th scope="col" className="whitespace-nowrap px-4 py-2.5 text-left text-xs font-medium text-muted-foreground">
                        {t("colExam")}
                      </th>
                      <th scope="col" className="whitespace-nowrap px-4 py-2.5 text-right text-xs font-medium text-muted-foreground">
                        {t("colQuestions")}
                      </th>
                      <th scope="col" className="whitespace-nowrap px-4 py-2.5 text-right text-xs font-medium text-muted-foreground">
                        {t("colMinutes")}
                      </th>
                      <th scope="col" className="whitespace-nowrap px-4 py-2.5 text-right text-xs font-medium text-muted-foreground">
                        {t("colPass")}
                      </th>
                      <th scope="col" className="whitespace-nowrap px-4 py-2.5 text-right text-xs font-medium text-muted-foreground">
                        {t("colBest")}
                      </th>
                      <th scope="col" className="whitespace-nowrap px-4 py-2.5 text-right text-xs font-medium text-muted-foreground">
                        {t("colAttempts")}
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    {exams.map((e) => (
                      <ExamTableRow key={e.id} exam={e} />
                    ))}
                    {kind === "mock" && (
                      <tr>
                        <td colSpan={6} className="px-4 py-3 text-muted-foreground">
                          <span className="flex items-center gap-2">
                            <Lock className="size-4 shrink-0" aria-hidden="true" />
                            {t("lockedMock")}
                          </span>
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </section>
          );
        })}
      </div>
    </div>
  );
}

function ExamTableRow({ exam }: { exam: ExamSummary }) {
  const t = useTranslations("exam");
  const loc = useLoc();
  const history = useProgress((s) => s.exams[exam.id]);
  const best = history?.length ? Math.max(...history.map((h) => h.score)) : undefined;
  const passed = history?.some((h) => h.passed);
  const href = exam.kind === "placement" ? "/placement/" : `/exam/${exam.id}/`;

  return (
    <tr className="transition-colors hover:bg-accent">
      <td className="px-4 py-3 align-middle">
        <Link
          href={href}
          className="font-bold text-foreground hover:text-primary focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring"
        >
          <Tx value={exam.title} />
        </Link>
        {exam.description && (
          <div className="mt-0.5 text-xs text-muted-foreground">{loc.t(exam.description)}</div>
        )}
      </td>
      <td className="whitespace-nowrap px-4 py-3 text-right font-mono tabular-nums text-muted-foreground">
        {exam.questionCount}
      </td>
      <td className="whitespace-nowrap px-4 py-3 text-right font-mono tabular-nums text-muted-foreground">
        {exam.duration_min}
      </td>
      <td className="whitespace-nowrap px-4 py-3 text-right font-mono tabular-nums text-muted-foreground">
        {percent(exam.pass_score)}
      </td>
      <td className="whitespace-nowrap px-4 py-3 text-right font-mono tabular-nums">
        {best !== undefined ? (
          <Badge variant={passed ? "success" : "muted"} className="font-mono tabular-nums">
            {percent(best)}
          </Badge>
        ) : (
          <span className="text-muted-foreground">{t("notTaken")}</span>
        )}
      </td>
      <td className="whitespace-nowrap px-4 py-3 text-right font-mono tabular-nums text-muted-foreground">
        {history?.length ?? 0}
      </td>
    </tr>
  );
}
