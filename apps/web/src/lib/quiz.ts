import type { Question } from "./types";

/** What the learner answered, per question type. */
export type UserAnswer =
  | { type: "mcq"; choice: number | null }
  | { type: "output"; text: string }
  | { type: "fill"; blanks: string[] }
  | { type: "parsons"; order: string[] };

export function emptyAnswer(q: Question): UserAnswer {
  switch (q.type) {
    case "mcq":
      return { type: "mcq", choice: null };
    case "output":
      return { type: "output", text: "" };
    case "fill":
      return { type: "fill", blanks: Array((q.code ?? "").split("___").length - 1).fill("") };
    case "parsons":
      return { type: "parsons", order: [] };
  }
}

const normOutput = (s: string) =>
  s
    .replace(/\r/g, "")
    .trim()
    .split("\n")
    .map((l) => l.replace(/\s+$/, ""))
    .join("\n");

const normToken = (s: string) => s.trim().replace(/\s+/g, " ").replace(/"/g, "'");

export function isAnswered(q: Question, a: UserAnswer): boolean {
  switch (a.type) {
    case "mcq":
      return a.choice !== null;
    case "output":
      return a.text.trim().length > 0;
    case "fill":
      return a.blanks.every((b) => b.trim().length > 0);
    case "parsons":
      return a.order.length === (q.lines?.length ?? 0);
  }
}

export function grade(q: Question, a: UserAnswer): boolean {
  switch (a.type) {
    case "mcq":
      return a.choice === q.answer;
    case "output":
      return normOutput(a.text) === normOutput(String(q.answer ?? ""));
    case "fill": {
      const expected = (q.answer as (string | string[])[]) ?? [];
      return expected.every((acc, i) => {
        const options = Array.isArray(acc) ? acc : [acc];
        return options.some((o) => normToken(o) === normToken(a.blanks[i] ?? ""));
      });
    }
    case "parsons":
      return JSON.stringify(a.order) === JSON.stringify(q.lines ?? []);
  }
}

/** Human readable correct answer, for feedback. */
export function correctAnswerText(q: Question, options?: string[]): string {
  switch (q.type) {
    case "mcq":
      return options?.[q.answer as number] ?? "";
    case "output":
      return String(q.answer ?? "");
    case "fill":
      return ((q.answer as (string | string[])[]) ?? []).map((a) => (Array.isArray(a) ? a[0] : a)).join(" · ");
    case "parsons":
      return (q.lines ?? []).join("\n");
  }
}
