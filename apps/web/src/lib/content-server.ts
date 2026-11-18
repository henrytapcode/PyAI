import "server-only";
import fs from "node:fs";
import path from "node:path";
import type { Exam, Lesson } from "./types";
import { capstones, catalog, readyLessons } from "./content";

const GENERATED = path.join(process.cwd(), "src", "generated");

function readJson<T>(...parts: string[]): T {
  return JSON.parse(fs.readFileSync(path.join(GENERATED, ...parts), "utf-8")) as T;
}

export function getLesson(id: string): Lesson {
  return readJson<Lesson>("lessons", `${id}.json`);
}

export function getExam(id: string): Exam {
  return readJson<Exam>("exams", `${id}.json`);
}

export const lessonIds = () => [
  ...readyLessons.map((l) => l.id),
  ...capstones.filter((c) => c.ready).map((c) => c.id),
];
export const examIds = () => catalog.exams.map((e) => e.id);
