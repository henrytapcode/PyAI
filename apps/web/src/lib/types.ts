// Shapes of the JSON produced by tools/build_content.py.

export type Locale = "en" | "vi";
export const LOCALES: Locale[] = ["vi", "en"];

/** A bilingual value. `vi` may be missing: the UI falls back to EN and shows "not translated". */
export type I18n<T = string> = { en: T; vi?: T };

export type QuestionType = "mcq" | "output" | "fill" | "parsons";

export interface QuestionText {
  prompt: string;
  options?: string[];
  explanation?: string;
}

export interface Question {
  id: string;
  type: QuestionType;
  tags: string[];
  difficulty?: number;
  code?: string;
  lines?: string[];
  answer?: number | string | (string | string[])[];
  /** false: keep mcq options in their written order. */
  shuffle_options?: boolean;
  en: QuestionText;
  vi?: QuestionText;
  lessonId?: string;
}

export interface Flashcard {
  id: string;
  code?: string;
  tags?: string[];
  en: { front: string; back: string };
  vi?: { front: string; back: string };
  lessonId?: string;
}

export interface Example {
  name: string;
  title: I18n;
  /** Walkthrough markdown per language. */
  explain: Partial<Record<Locale, string>>;
  code: string;
  output: string;
}

export interface Alternative {
  name: string;
  title: I18n;
  explain: Partial<Record<Locale, string>>;
  code: string;
}

export type ExerciseKind = "code" | "fill" | "debug" | "project";

export interface Exercise {
  id: string;
  kind: ExerciseKind;
  title: I18n;
  difficulty: number;
  tags: string[];
  hints: I18n<string[]>;
  prompt: Partial<Record<Locale, string>>;
  starter: string;
  solution: string;
  tests: string;
  solution_unlock_attempts: number;
  alternatives: Alternative[];
}

export interface LessonMeta {
  id: string;
  phase: string;
  order: number;
  kind: "lesson" | "project";
  title: I18n;
  summary: I18n;
  level: string;
  tags: string[];
  prerequisites: string[];
  duration_min: number;
  outcomes: I18n<string[]>;
  review_by: string;
  further_reading?: { title: I18n; url: string }[];
}

export interface Lesson {
  meta: LessonMeta;
  body: Partial<Record<Locale, string>>;
  examples: Example[];
  exercises: Exercise[];
  quiz: { questions: Question[]; flashcards: Flashcard[] };
}

export interface LessonSummary {
  id: string;
  order: number;
  kind: "lesson" | "project";
  title: I18n;
  summary?: I18n;
  outcomes?: I18n<string[]>;
  prerequisites: string[];
  ready: boolean;
  duration?: number;
  tags?: string[];
  exerciseIds?: string[];
  questionCount?: number;
}

export interface Phase {
  id: string;
  order: number;
  icon: string;
  title: I18n;
  summary: I18n;
  runner?: "local";
  skippable_by_placement?: boolean;
  lessons: LessonSummary[];
}

export type ExamKind = "phase_test" | "placement" | "mock";

export interface ExamSummary {
  id: string;
  kind: ExamKind;
  phase?: string;
  title: I18n;
  description?: I18n;
  duration_min: number;
  pass_score: number;
  questionCount: number;
  skips_phases: string[];
}

export interface Exam extends Omit<ExamSummary, "questionCount"> {
  questions: Question[];
}

export interface Catalog {
  phases: Phase[];
  topics: Record<string, I18n>;
  exams: ExamSummary[];
  capstones: { id: string; title: I18n }[];
  furtherReading?: I18n<string[]>;
}

export interface GlossaryTerm {
  term: string;
  vi_term?: string;
  tags?: string[];
  en: string;
  vi?: string;
  example?: string;
  in_practice?: I18n;
  related?: string[];
}

export type InterviewKind = "concept" | "coding" | "scenario" | "system";

export interface InterviewQuestion {
  id: string;
  topic: string;
  level: "junior" | "mid";
  kind?: InterviewKind;
  code?: string;
  en: { question: string; answer: string; tip?: string };
  vi?: { question: string; answer: string; tip?: string };
}

export interface PortfolioProject {
  id: string;
  lesson?: string;
  phase?: string;
  difficulty: number;
  tags?: string[];
  title: I18n;
  pitch: I18n;
  cv_bullet: I18n;
  skills: string[];
  stretch?: I18n<string[]>;
}

/** Output of tools/pyrunner/tracer.py (the Visualize view). */
export interface TraceVar {
  name: string;
  type: string;
  repr: string;
}

export interface TraceStep {
  line: number;
  event: "line" | "return" | "exception";
  stack: { name: string; vars: TraceVar[] }[];
  out: number;
  ret?: string;
}

export interface TraceResult {
  steps: TraceStep[];
  stdout: string;
  error: { type: string; message: string; line: number | null } | null;
  truncated: boolean;
  timedOut?: boolean;
}

export interface TestCaseResult {
  name: string;
  label: string;
  status: "passed" | "failed" | "error";
  message: string | null;
  line: number | null;
}

export interface TestRunResult {
  ok: boolean;
  passed: number;
  total: number;
  tests: TestCaseResult[];
  error: { type: string; message: string; line: number | null } | null;
  stdout: string;
  timedOut?: boolean;
}
