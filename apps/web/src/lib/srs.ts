import { addDays, todayKey } from "./utils";

/** Spaced repetition state per card (SM-2, simplified). */
export interface SrsCard {
  ease: number;
  interval: number; // days
  reps: number;
  lapses: number;
  due: string; // yyyy-mm-dd
  last?: string;
}

export type Grade = "again" | "hard" | "good" | "easy";

export function newCard(today = todayKey()): SrsCard {
  return { ease: 2.5, interval: 0, reps: 0, lapses: 0, due: today };
}

export function schedule(card: SrsCard, grade: Grade, today = todayKey()): SrsCard {
  let { ease, interval, reps, lapses } = card;
  if (grade === "again") {
    lapses += 1;
    reps = 0;
    interval = 0; // see it again today
    ease = Math.max(1.3, ease - 0.2);
  } else {
    reps += 1;
    if (grade === "hard") ease = Math.max(1.3, ease - 0.15);
    if (grade === "easy") ease += 0.15;
    if (reps === 1) interval = grade === "easy" ? 3 : 1;
    else if (reps === 2) interval = grade === "hard" ? 3 : 6;
    else interval = Math.round(interval * (grade === "hard" ? 1.2 : ease) * (grade === "easy" ? 1.3 : 1));
  }
  return { ease, interval, reps, lapses, due: addDays(today, interval), last: today };
}

export function isDue(card: SrsCard | undefined, today = todayKey()): boolean {
  return !!card && card.due <= today;
}

/** Preview the next interval for a grade (shown on the buttons). */
export function previewInterval(card: SrsCard, grade: Grade): number {
  return schedule(card, grade).interval;
}
