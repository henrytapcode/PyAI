"use client";

import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import { activeStorage, PROGRESS_KEY } from "./storage";
import { newCard, schedule, type Grade, type SrsCard } from "./srs";
import type { Locale } from "./types";
import { todayKey } from "./utils";

export interface ExerciseProgress {
  code?: string;
  attempts: number;
  passed: boolean;
  passedAt?: string;
  hintsShown: number;
  solutionViewed?: boolean;
  lastPassed?: number;
  lastTotal?: number;
}

export interface ExamAttempt {
  date: string;
  score: number;
  passed: boolean;
  durationSec: number;
  byTopic: Record<string, { correct: number; total: number }>;
}

export interface ProgressData {
  version: 1;
  profile: {
    locale: Locale;
    track: "A" | "B" | null;
    onboarded: boolean;
    createdAt: string;
    dailyGoal: number;
  };
  lessons: Record<string, { theoryDone?: boolean; visitedAt?: string; completedAt?: string }>;
  exercises: Record<string, ExerciseProgress>;
  quizzes: Record<string, { best: number; last: number; attempts: number }>;
  questionStats: Record<string, { correct: number; wrong: number; tags: string[] }>;
  srs: Record<string, SrsCard>;
  exams: Record<string, ExamAttempt[]>;
  placement: { score: number; passed: boolean; date: string } | null;
  skippedPhases: string[];
  activity: Record<string, number>;
  xp: number;
  /** Interview questions the learner marked as practiced. */
  practiced: Record<string, boolean>;
}

export interface AnswerRecord {
  questionId: string;
  correct: boolean;
  tags: string[];
}

interface Actions {
  setLocale(locale: Locale): void;
  setTrack(track: "A" | "B"): void;
  finishOnboarding(): void;
  setDailyGoal(goal: number): void;
  visitLesson(id: string): void;
  markTheory(id: string, flashcardIds: string[]): void;
  saveCode(exerciseId: string, code: string): void;
  recordCheck(exerciseId: string, passed: number, total: number): void;
  showHint(exerciseId: string): void;
  viewSolution(exerciseId: string): void;
  recordQuiz(lessonId: string, score: number, answers: AnswerRecord[], flashcardIds: string[]): void;
  reviewCard(key: string, grade: Grade): void;
  recordExam(examId: string, attempt: ExamAttempt, answers: AnswerRecord[], skipsPhases?: string[], isPlacement?: boolean): void;
  markLessonComplete(id: string): void;
  togglePracticed(id: string): void;
  importData(data: ProgressData): void;
  reset(): void;
}

export type ProgressStore = ProgressData & Actions;

export const initialProgress = (): ProgressData => ({
  version: 1,
  profile: { locale: "vi", track: null, onboarded: false, createdAt: todayKey(), dailyGoal: 30 },
  lessons: {},
  exercises: {},
  quizzes: {},
  questionStats: {},
  srs: {},
  exams: {},
  placement: null,
  skippedPhases: [],
  activity: {},
  xp: 0,
  practiced: {},
});

export const XP = { theory: 10, exercise: 20, exerciseWithSolution: 5, quiz: 30, review: 2, exam: 50 } as const;

function gain(state: ProgressData, amount: number): Pick<ProgressData, "xp" | "activity"> {
  const day = todayKey();
  return { xp: state.xp + amount, activity: { ...state.activity, [day]: (state.activity[day] ?? 0) + amount } };
}

function addCards(srs: Record<string, SrsCard>, keys: string[]): Record<string, SrsCard> {
  const next = { ...srs };
  for (const k of keys) if (!next[k]) next[k] = newCard();
  return next;
}

function applyAnswers(state: ProgressData, answers: AnswerRecord[]) {
  const questionStats = { ...state.questionStats };
  let srs = { ...state.srs };
  for (const a of answers) {
    const prev = questionStats[a.questionId] ?? { correct: 0, wrong: 0, tags: a.tags };
    questionStats[a.questionId] = {
      correct: prev.correct + (a.correct ? 1 : 0),
      wrong: prev.wrong + (a.correct ? 0 : 1),
      tags: a.tags,
    };
    // Missed questions join the review deck, due today.
    if (!a.correct) srs = addCards(srs, [`q:${a.questionId}`]);
  }
  return { questionStats, srs };
}

const EX_DEFAULT: ExerciseProgress = { attempts: 0, passed: false, hintsShown: 0 };

export const useProgress = create<ProgressStore>()(
  persist(
    (set, get) => ({
      ...initialProgress(),

      setLocale: (locale) => set((s) => ({ profile: { ...s.profile, locale } })),
      setTrack: (track) => set((s) => ({ profile: { ...s.profile, track } })),
      finishOnboarding: () => set((s) => ({ profile: { ...s.profile, onboarded: true } })),
      setDailyGoal: (dailyGoal) => set((s) => ({ profile: { ...s.profile, dailyGoal } })),

      visitLesson: (id) =>
        set((s) => ({ lessons: { ...s.lessons, [id]: { ...s.lessons[id], visitedAt: new Date().toISOString() } } })),

      markTheory: (id, flashcardIds) =>
        set((s) => {
          if (s.lessons[id]?.theoryDone) return {};
          return {
            lessons: { ...s.lessons, [id]: { ...s.lessons[id], theoryDone: true } },
            srs: addCards(s.srs, flashcardIds.map((f) => `card:${f}`)),
            ...gain(s, XP.theory),
          };
        }),

      saveCode: (exerciseId, code) =>
        set((s) => ({
          exercises: { ...s.exercises, [exerciseId]: { ...EX_DEFAULT, ...s.exercises[exerciseId], code } },
        })),

      recordCheck: (exerciseId, passed, total) =>
        set((s) => {
          const prev = { ...EX_DEFAULT, ...s.exercises[exerciseId] };
          const nowPassed = total > 0 && passed === total;
          const firstPass = nowPassed && !prev.passed;
          const next: ExerciseProgress = {
            ...prev,
            attempts: prev.attempts + 1,
            passed: prev.passed || nowPassed,
            passedAt: firstPass ? new Date().toISOString() : prev.passedAt,
            lastPassed: passed,
            lastTotal: total,
          };
          const reward = firstPass ? (prev.solutionViewed ? XP.exerciseWithSolution : XP.exercise) : 1;
          return { exercises: { ...s.exercises, [exerciseId]: next }, ...gain(s, reward) };
        }),

      showHint: (exerciseId) =>
        set((s) => {
          const prev = { ...EX_DEFAULT, ...s.exercises[exerciseId] };
          return { exercises: { ...s.exercises, [exerciseId]: { ...prev, hintsShown: Math.min(3, prev.hintsShown + 1) } } };
        }),

      viewSolution: (exerciseId) =>
        set((s) => ({
          exercises: { ...s.exercises, [exerciseId]: { ...EX_DEFAULT, ...s.exercises[exerciseId], solutionViewed: true } },
        })),

      recordQuiz: (lessonId, score, answers, flashcardIds) =>
        set((s) => {
          const prev = s.quizzes[lessonId] ?? { best: 0, last: 0, attempts: 0 };
          const applied = applyAnswers(s, answers);
          return {
            quizzes: { ...s.quizzes, [lessonId]: { best: Math.max(prev.best, score), last: score, attempts: prev.attempts + 1 } },
            questionStats: applied.questionStats,
            srs: addCards(applied.srs, flashcardIds.map((f) => `card:${f}`)),
            ...gain(s, Math.round(XP.quiz * score)),
          };
        }),

      reviewCard: (key, grade) =>
        set((s) => {
          const card = s.srs[key] ?? newCard();
          let questionStats = s.questionStats;
          if (key.startsWith("q:")) {
            const qid = key.slice(2);
            const prev = s.questionStats[qid];
            if (prev) {
              const ok = grade !== "again";
              questionStats = {
                ...s.questionStats,
                [qid]: { ...prev, correct: prev.correct + (ok ? 1 : 0), wrong: prev.wrong + (ok ? 0 : 1) },
              };
            }
          }
          return { srs: { ...s.srs, [key]: schedule(card, grade) }, questionStats, ...gain(s, XP.review) };
        }),

      recordExam: (examId, attempt, answers, skipsPhases = [], isPlacement = false) =>
        set((s) => {
          const applied = applyAnswers(s, answers);
          const update: Partial<ProgressData> = {
            exams: { ...s.exams, [examId]: [...(s.exams[examId] ?? []), attempt] },
            ...applied,
            ...gain(s, Math.round(XP.exam * attempt.score)),
          };
          if (isPlacement) {
            update.placement = { score: attempt.score, passed: attempt.passed, date: attempt.date };
            if (attempt.passed) update.skippedPhases = Array.from(new Set([...s.skippedPhases, ...skipsPhases]));
          }
          return update;
        }),

      markLessonComplete: (id) =>
        set((s) =>
          s.lessons[id]?.completedAt
            ? {}
            : { lessons: { ...s.lessons, [id]: { ...s.lessons[id], completedAt: new Date().toISOString() } } },
        ),

      togglePracticed: (id) => set((s) => ({ practiced: { ...s.practiced, [id]: !s.practiced[id] } })),

      importData: (data) => set(() => ({ ...initialProgress(), ...data })),
      reset: () => set(() => initialProgress()),
    }),
    {
      name: PROGRESS_KEY,
      version: 1,
      storage: createJSONStorage(() => activeStorage),
      partialize: (s) => {
        // Persist data only, not actions.
        const data: Record<string, unknown> = {};
        for (const k of Object.keys(initialProgress())) data[k] = s[k as keyof ProgressData];
        return data as unknown as ProgressStore;
      },
    },
  ),
);

export function exportProgress(): string {
  const s = useProgress.getState();
  const data: Record<string, unknown> = {};
  for (const k of Object.keys(initialProgress())) data[k] = s[k as keyof ProgressData];
  return JSON.stringify({ app: "python-ai-platform", exportedAt: new Date().toISOString(), data }, null, 2);
}

export function parseImport(text: string): ProgressData {
  const parsed = JSON.parse(text);
  const data = parsed?.data ?? parsed;
  if (!data || data.version !== 1 || typeof data.profile !== "object") {
    throw new Error("invalid progress file");
  }
  return data as ProgressData;
}
