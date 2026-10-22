import { ExamRunner } from "@/components/exam-runner";
import { examIds, getExam } from "@/lib/content-server";

export const dynamicParams = false;

export function generateStaticParams() {
  return examIds().map((id) => ({ id }));
}

export default async function ExamPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <ExamRunner exam={getExam(id)} />;
}
