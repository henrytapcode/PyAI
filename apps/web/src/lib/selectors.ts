import { allLessons, catalog, readyLessons } from "./content";
import type { ProgressData } from "./progress";
import { isDue } from "./srs";
import type { LessonSummary, Phase } from "./types";
import { addDays, todayKey } from "./utils";

export const QUIZ_PASS = 0.7;
export const MASTERY = 0.8;

export type LessonStatus = "locked" | "available" | "in_progress" | "completed" | "skipped" | "coming_soon";

export function lessonParts(p: ProgressData, l: LessonSummary) {
  const exIds = l.exerciseIds ?? [];
  const exPassed = exIds.filter((id) => p.exercises[id]?.passed).length;
  const quizBest = p.quizzes[l.id]?.best ?? 0;
  const theory = !!p.lessons[l.id]?.theoryDone;
  const parts = [theory ? 1 : 0, exIds.length ? exPassed / exIds.length : 1, Math.min(1, quizBest / QUIZ_PASS)];
  return {
    theory,
    exPassed,
    exTotal: exIds.length,
    quizBest,
    quizDone: quizBest >= QUIZ_PASS,
    fraction: parts.reduce((a, b) => a + b, 0) / parts.length,
  };
}

export function isLessonComplete(p: ProgressData, l: LessonSummary): boolean {
  const parts = lessonParts(p, l);
  return parts.theory && parts.exPassed === parts.exTotal && parts.quizDone;
}

export function lessonStatus(p: ProgressData, l: LessonSummary & { phaseId?: string }): LessonStatus {
  if (!l.ready) return "coming_soon";
  if (isLessonComplete(p, l)) return "completed";
  const phaseId = l.phaseId ?? l.id.split("-")[0];
  if (p.skippedPhases.includes(phaseId)) return "skipped";
  const parts = lessonParts(p, l);
  if (parts.fraction > 0 || p.lessons[l.id]?.visitedAt) return "in_progress";
  const prereqsMet = l.prerequisites.every((pre) => {
    const pl = allLessons.find((x) => x.id === pre);
    if (!pl) return true;
    if (!pl.ready) return true; // don't block on lessons that don't exist yet
    return isLessonComplete(p, pl) || p.skippedPhases.includes(pl.phaseId);
  });
  // Soft lock: "locked" is a recommendation, the learner can still open the lesson.
  return prereqsMet ? "available" : "locked";
}

export function phaseProgress(p: ProgressData, phase: Phase) {
  const ready = phase.lessons.filter((l) => l.ready);
  const done = ready.filter((l) => isLessonComplete(p, l)).length;
  const exIds = ready.flatMap((l) => l.exerciseIds ?? []);
  const exDone = exIds.filter((id) => p.exercises[id]?.passed).length;
  const test = catalog.exams.find((e) => e.kind === "phase_test" && e.phase === phase.id);
  const testAttempts = test ? p.exams[test.id] ?? [] : [];
  return {
    ready: ready.length,
    total: phase.lessons.length,
    done,
    fraction: ready.length ? ready.reduce((a, l) => a + lessonParts(p, l).fraction, 0) / ready.length : 0,
    exerciseRate: exIds.length ? exDone / exIds.length : 0,
    phaseTest: test,
    phaseTestPassed: testAttempts.some((a) => a.passed),
    skipped: p.skippedPhases.includes(phase.id),
  };
}

export function nextLesson(p: ProgressData) {
  const inProgress = readyLessons
    .filter((l) => lessonStatus(p, l) === "in_progress")
    .sort((a, b) => (p.lessons[b.id]?.visitedAt ?? "").localeCompare(p.lessons[a.id]?.visitedAt ?? ""));
  if (inProgress[0]) return inProgress[0];
  return readyLessons.find((l) => ["available", "locked"].includes(lessonStatus(p, l)));
}

export function streak(p: ProgressData, today = todayKey()): number {
  let count = 0;
  let day = p.activity[today] ? today : addDays(today, -1);
  while (p.activity[day]) {
    count += 1;
    day = addDays(day, -1);
  }
  return count;
}

export function dueKeys(p: ProgressData, today = todayKey()): string[] {
  return Object.entries(p.srs)
    .filter(([, c]) => isDue(c, today))
    .sort(([, a], [, b]) => a.due.localeCompare(b.due))
    .map(([k]) => k);
}

export function topicAccuracy(p: ProgressData) {
  const byTopic: Record<string, { correct: number; total: number }> = {};
  for (const s of Object.values(p.questionStats)) {
    const topic = s.tags[0];
    if (!topic) continue;
    byTopic[topic] ??= { correct: 0, total: 0 };
    byTopic[topic].correct += s.correct;
    byTopic[topic].total += s.correct + s.wrong;
  }
  return Object.entries(byTopic)
    .map(([topic, v]) => ({ topic, ...v, rate: v.total ? v.correct / v.total : 0 }))
    .sort((a, b) => a.rate - b.rate);
}

export function weakTopics(p: ProgressData) {
  return topicAccuracy(p).filter((t) => t.total >= 3 && t.rate < 0.7);
}

export function overallProgress(p: ProgressData) {
  const ready = readyLessons;
  const done = ready.filter((l) => isLessonComplete(p, l)).length;
  const exIds = ready.flatMap((l) => l.exerciseIds ?? []);
  return {
    lessonsDone: done,
    lessonsReady: ready.length,
    lessonsTotal: allLessons.length,
    exercisesPassed: exIds.filter((id) => p.exercises[id]?.passed).length,
    exercisesTotal: exIds.length,
  };
}

/** Last N days of activity, oldest first, for the heatmap. */
export function activityDays(p: ProgressData, days = 84, today = todayKey()) {
  return Array.from({ length: days }, (_, i) => {
    const key = addDays(today, i - days + 1);
    return { key, xp: p.activity[key] ?? 0 };
  });
}
