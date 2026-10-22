"""Build curriculum/ into static JSON for the web app.

Output (gitignored):
  apps/web/src/generated/catalog.json        phases, lessons (summary), topics, exams list
  apps/web/src/generated/lessons/<id>.json   full lesson: markdown, examples, exercises, quiz
  apps/web/src/generated/exams/<id>.json     phase tests, placement, mock exams
  apps/web/src/generated/review.json         every flashcard + question (for spaced repetition)
  apps/web/src/generated/glossary.json, interview.json
  apps/web/public/pyrunner/runner.py         browser test runner (same file the validator uses)
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM = ROOT / "curriculum"
WEB = ROOT / "apps" / "web"
OUT = WEB / "src" / "generated"


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def read(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def i18n_files(folder: Path, stem: str) -> dict:
    return {lang: text for lang in ("en", "vi") if (text := read(folder / f"{stem}.{lang}.md")) is not None}


def build_example(py: Path) -> dict:
    code = py.read_text(encoding="utf-8")
    first = code.splitlines()[0] if code else ""
    title = first.lstrip("# ").strip() if first.startswith("#") else py.stem.replace("_", " ")
    return {"name": py.stem, "title": title, "code": code, "output": read(py.with_suffix(".out")) or ""}


def build_exercise(ex_dir: Path) -> dict:
    meta = load_yaml(ex_dir / "exercise.yaml")
    return {
        **meta,
        "prompt": i18n_files(ex_dir, "prompt"),
        "starter": read(ex_dir / "starter.py") or "",
        "solution": read(ex_dir / "solution.py") or "",
        "tests": read(ex_dir / "test_exercise.py") or "",
        "solution_unlock_attempts": meta.get("solution_unlock_attempts", 3),
    }


def build_lesson(lesson_dir: Path) -> dict:
    meta = load_yaml(lesson_dir / "meta.yaml")
    ex_root = lesson_dir / "exercises"
    exercises = [build_exercise(d) for d in sorted(ex_root.iterdir()) if (d / "exercise.yaml").exists()] if ex_root.exists() else []
    quiz = load_yaml(lesson_dir / "quiz.yaml") if (lesson_dir / "quiz.yaml").exists() else {"questions": [], "flashcards": []}
    examples = [build_example(p) for p in sorted((lesson_dir / "examples").glob("*.py"))]
    return {
        "meta": {"kind": "lesson", "prerequisites": [], **meta},
        "body": i18n_files(lesson_dir, "lesson"),
        "examples": examples,
        "exercises": exercises,
        "quiz": quiz,
    }


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    syllabus = load_yaml(CURRICULUM / "syllabus.yaml")
    topics = load_yaml(CURRICULUM / "topics.yaml")["topics"]

    review = {"flashcards": [], "questions": []}
    phases = []
    lesson_count = 0
    for phase in syllabus["phases"]:
        phase_dir = CURRICULUM / phase["dir"]
        lessons = []
        for order, item in enumerate(phase["lessons"], 1):
            lesson_dir = phase_dir / item["id"]
            ready = (lesson_dir / "meta.yaml").exists()
            summary = {
                "id": item["id"],
                "order": order,
                "kind": item.get("kind", "lesson"),
                "title": item["title"],
                "outcomes": item.get("outcomes"),
                "prerequisites": item.get("prerequisites", []),
                "ready": ready,
            }
            if ready:
                try:
                    lesson = build_lesson(lesson_dir)
                except Exception as exc:  # noqa: BLE001 - half-written lesson: skip, don't break the app
                    print(f"WARN skipping {item['id']}: {exc}", file=sys.stderr)
                    summary["ready"] = False
                    lessons.append(summary)
                    continue
                write_json(OUT / "lessons" / f"{item['id']}.json", lesson)
                lesson_count += 1
                meta = lesson["meta"]
                summary.update(
                    title=meta["title"],
                    summary=meta["summary"],
                    outcomes=meta["outcomes"],
                    prerequisites=meta.get("prerequisites", []),
                    duration=meta["duration_min"],
                    tags=meta["tags"],
                    exerciseIds=[e["id"] for e in lesson["exercises"]],
                    questionCount=len(lesson["quiz"]["questions"]),
                )
                for card in lesson["quiz"]["flashcards"]:
                    review["flashcards"].append({**card, "lessonId": item["id"]})
                for q in lesson["quiz"]["questions"]:
                    review["questions"].append({**q, "lessonId": item["id"]})
            lessons.append(summary)
        phases.append({k: v for k, v in phase.items() if k not in ("lessons", "dir")} | {"lessons": lessons})

    exams = []
    exam_files = sorted(CURRICULUM.glob("*/phase-test.yaml")) + sorted((CURRICULUM / "placement").glob("*.yaml")) \
        + sorted((CURRICULUM / "exams").glob("*.yaml"))
    for path in exam_files:
        exam = load_yaml(path)
        write_json(OUT / "exams" / f"{exam['id']}.json", exam)
        exams.append({
            "id": exam["id"], "kind": exam["kind"], "phase": exam.get("phase"), "title": exam["title"],
            "description": exam.get("description"), "duration_min": exam["duration_min"],
            "pass_score": exam["pass_score"], "questionCount": len(exam["questions"]),
            "skips_phases": exam.get("skips_phases", []),
        })

    write_json(OUT / "catalog.json", {
        "phases": phases,
        "topics": topics,
        "exams": exams,
        "capstones": syllabus.get("capstones", []),
        "furtherReading": syllabus.get("further_reading"),
    })
    write_json(OUT / "review.json", review)
    glossary = load_yaml(CURRICULUM / "glossary.yaml") if (CURRICULUM / "glossary.yaml").exists() else {"terms": []}
    write_json(OUT / "glossary.json", glossary)
    interview_path = CURRICULUM / "interview" / "questions.yaml"
    write_json(OUT / "interview.json", load_yaml(interview_path) if interview_path.exists() else {"questions": []})
    # Keep lessons/ and exams/ importable even when empty.
    (OUT / "lessons").mkdir(parents=True, exist_ok=True)
    (OUT / "exams").mkdir(parents=True, exist_ok=True)

    runner_dst = WEB / "public" / "pyrunner" / "runner.py"
    runner_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / "tools" / "pyrunner" / "runner.py", runner_dst)

    print(f"Built {lesson_count} lessons, {len(exams)} exams, "
          f"{len(review['flashcards'])} flashcards, {len(review['questions'])} questions -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
