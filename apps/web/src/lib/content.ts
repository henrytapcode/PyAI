import catalogJson from "@/generated/catalog.json";
import type { Catalog, LessonSummary, Phase } from "./types";

// The catalog is small, so it is bundled for client components too.
export const catalog = catalogJson as unknown as Catalog;

export const allLessons: (LessonSummary & { phaseId: string })[] = catalog.phases.flatMap((p) =>
  p.lessons.map((l) => ({ ...l, phaseId: p.id })),
);

export const readyLessons = allLessons.filter((l) => l.ready);

export function findLesson(id: string) {
  return allLessons.find((l) => l.id === id);
}

export function findPhase(id: string): Phase | undefined {
  return catalog.phases.find((p) => p.id === id);
}

export function phaseOfLesson(lessonId: string): Phase | undefined {
  return catalog.phases.find((p) => p.lessons.some((l) => l.id === lessonId));
}

/** Next / previous ready lesson in syllabus order. */
export function neighbours(lessonId: string) {
  const i = readyLessons.findIndex((l) => l.id === lessonId);
  return { prev: i > 0 ? readyLessons[i - 1] : undefined, next: i >= 0 ? readyLessons[i + 1] : undefined };
}
