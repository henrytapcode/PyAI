import { LessonView } from "@/components/lesson/lesson-view";
import { getLesson, lessonIds } from "@/lib/content-server";

export const dynamicParams = false;

export function generateStaticParams() {
  return lessonIds().map((id) => ({ id }));
}

export default async function LessonPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const lesson = getLesson(id);
  return <LessonView lesson={lesson} />;
}
