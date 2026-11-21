"""Build curriculum/ into static JSON for the web app.

Output (gitignored):
  apps/web/src/generated/catalog.json        phases, lessons (summary), topics, exams list
  apps/web/src/generated/lessons/<id>.json   full lesson: markdown, examples, exercises, quiz
  apps/web/src/generated/exams/<id>.json     phase tests, placement, mock exams
  apps/web/src/generated/review.json         every flashcard + question (for spaced repetition)
  apps/web/src/generated/glossary.json, interview.json, portfolio.json
  apps/web/public/pyrunner/runner.py         browser test runner (same file the validator uses)
  apps/web/public/pyrunner/tracer.py         step-through tracer for the "Visualize" view
  apps/web/public/pyrunner/llm.py            deterministic fake LLM client (`pyai_llm`)
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

import yaml

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM = ROOT / "curriculum"
WEB = ROOT / "apps" / "web"
OUT = WEB / "src" / "generated"

LOCAL_ONLY_MODULES = ("torch", "transformers", "fastapi", "uvicorn")
_LOCAL_IMPORT_RE = re.compile(
    rf"^\s*(?:import|from)\s+(?:{'|'.join(LOCAL_ONLY_MODULES)})\b",
    re.MULTILINE,
)


def question_runner(q: dict) -> str | None:
    """Return 'local' when a question imports a local-only module, else None."""
    text = f"{q.get('code') or ''}\n" + "\n".join(q.get("lines") or [])
    return "local" if _LOCAL_IMPORT_RE.search(text) else None


def attach_question_runners(questions: list[dict]) -> list[dict]:
    """Attach runner='local' in place on questions that need the local runner."""
    for q in questions:
        if runner := question_runner(q):
            q["runner"] = runner
    return questions


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


def explained(py: Path) -> tuple[dict, dict]:
    """Read ``<stem>.<lang>.md`` next to a code file: '# Title' line, then the explanation."""
    titles, bodies = {}, {}
    for lang in ("en", "vi"):
        text = read(py.with_suffix(f".{lang}.md"))
        if text is None:
            continue
        lines = text.lstrip().splitlines()
        if lines and lines[0].startswith("# "):
            titles[lang] = lines[0][2:].strip()
            lines = lines[1:]
        bodies[lang] = "\n".join(lines).strip()
    return titles, bodies


def build_example(py: Path) -> dict:
    code = py.read_text(encoding="utf-8")
    titles, bodies = explained(py)
    if "en" not in titles:
        first = code.splitlines()[0] if code else ""
        titles["en"] = first.lstrip("# ").strip() if first.startswith("#") else py.stem.replace("_", " ")
    return {"name": py.stem, "title": titles, "explain": bodies, "code": code, "output": read(py.with_suffix(".out")) or ""}


def build_alternative(py: Path) -> dict:
    titles, bodies = explained(py)
    titles.setdefault("en", py.stem.replace("_", " "))
    return {"name": py.stem, "title": titles, "explain": bodies, "code": py.read_text(encoding="utf-8")}


def build_exercise(ex_dir: Path) -> dict:
    meta = load_yaml(ex_dir / "exercise.yaml")
    alt_dir = ex_dir / "alternatives"
    return {
        **meta,
        "alternatives": [build_alternative(a) for a in sorted(alt_dir.glob("*.py"))] if alt_dir.exists() else [],
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
    attach_question_runners(quiz.get("questions", []))
    examples = [build_example(p) for p in sorted((lesson_dir / "examples").glob("*.py"))]
    return {
        "meta": {"kind": "lesson", "prerequisites": [], **meta},
        "body": i18n_files(lesson_dir, "lesson"),
        "examples": examples,
        "exercises": exercises,
        "quiz": quiz,
    }


def lesson_groups(syllabus: dict) -> list[dict]:
    """Return syllabus phases followed by a synthetic 'cap' group for capstones."""
    return [
        *syllabus["phases"],
        {"id": "cap", "dir": "capstones", "lessons": syllabus.get("capstones") or []},
    ]


def _truncate(text: str, limit: int = 160) -> str:
    """Collapse whitespace and trim text to `limit` characters with an ellipsis."""
    cleaned = " ".join(text.split())
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[: limit - 1].rstrip()}…"


def _truncate_i18n(value: dict | None, limit: int = 160) -> dict | None:
    if not value:
        return None
    truncated = {k: _truncate(v, limit) for k, v in value.items() if isinstance(v, str) and v}
    return truncated or None


def _search_item(
    *,
    item_id: str,
    kind: str,
    title: dict,
    href: str,
    tags: list[str],
    subtitle: dict | None = None,
    phase: str | None = None,
) -> dict:
    entry: dict = {
        "id": item_id,
        "kind": kind,
        "title": title,
        "href": href,
        "tags": tags,
    }
    if subtitle:
        entry["subtitle"] = subtitle
    if phase:
        entry["phase"] = phase
    return entry


def build_lesson_summary(
    item: dict,
    order: int,
    group_dir: Path,
    out: Path,
    review: dict,
    *,
    phase: str | None = None,
    search_items: list[dict] | None = None,
) -> tuple[dict, bool]:
    """Build one lesson/capstone summary and write its lesson JSON when ready."""
    lesson_dir = group_dir / item["id"]
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
    if item.get("runner"):
        summary["runner"] = item["runner"]
    if not ready:
        return summary, False
    try:
        lesson = build_lesson(lesson_dir)
    except Exception as exc:  # noqa: BLE001 - half-written lesson: skip, don't break the app
        print(f"WARN skipping {item['id']}: {exc}", file=sys.stderr)
        summary["ready"] = False
        return summary, False
    if item.get("runner"):
        lesson["meta"]["runner"] = item["runner"]
    write_json(out / "lessons" / f"{item['id']}.json", lesson)
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
    if search_items is not None:
        lesson_id = item["id"]
        search_items.append(
            _search_item(
                item_id=f"lesson:{lesson_id}",
                kind="lesson",
                title=meta["title"],
                subtitle=_truncate_i18n(meta.get("summary")),
                href=f"/lesson/{lesson_id}/",
                tags=list(meta.get("tags") or []),
                phase=phase,
            )
        )
        for ex in lesson["exercises"]:
            search_items.append(
                _search_item(
                    item_id=f"exercise:{ex['id']}",
                    kind="exercise",
                    title=ex["title"],
                    subtitle=_truncate_i18n(meta["title"]),
                    href=f"/lesson/{lesson_id}/?tab=exercises&ex={quote(ex['id'], safe='')}",
                    tags=list(ex.get("tags") or []),
                    phase=phase,
                )
            )
    return summary, True


def main(curriculum: Path = CURRICULUM, out: Path = OUT, web: Path | None = WEB) -> int:
    if out.exists():
        shutil.rmtree(out)
    syllabus = load_yaml(curriculum / "syllabus.yaml")
    topics_path = curriculum / "topics.yaml"
    topics = load_yaml(topics_path)["topics"] if topics_path.exists() else []

    review = {"flashcards": [], "questions": []}
    search_items: list[dict] = []
    phases = []
    capstones = []
    lesson_count = 0
    for group in lesson_groups(syllabus):
        group_dir = curriculum / group["dir"]
        summaries = []
        for order, item in enumerate(group["lessons"], 1):
            summary, built = build_lesson_summary(
                item,
                order,
                group_dir,
                out,
                review,
                phase=group["id"],
                search_items=search_items,
            )
            if built:
                lesson_count += 1
            summaries.append(summary)
        if group["id"] == "cap":
            capstones = summaries
        else:
            phase_meta = {k: v for k, v in group.items() if k not in ("lessons", "dir", "runner")}
            phases.append(phase_meta | {"lessons": summaries})

    exams = []
    exam_files = (
        sorted(curriculum.glob("*/phase-test.yaml"))
        + sorted((curriculum / "placement").glob("*.yaml"))
        + sorted((curriculum / "exams").glob("*.yaml"))
    )
    for path in exam_files:
        exam = load_yaml(path)
        attach_question_runners(exam.get("questions", []))
        write_json(out / "exams" / f"{exam['id']}.json", exam)
        exams.append({
            "id": exam["id"], "kind": exam["kind"], "phase": exam.get("phase"),
            "title": exam["title"], "description": exam.get("description"),
            "duration_min": exam["duration_min"], "pass_score": exam["pass_score"],
            "questionCount": len(exam["questions"]),
            "skips_phases": exam.get("skips_phases", []),
        })

    write_json(out / "catalog.json", {
        "phases": phases,
        "topics": topics,
        "exams": exams,
        "capstones": capstones,
        "furtherReading": syllabus.get("further_reading"),
    })
    write_json(out / "review.json", review)
    glossary_path = curriculum / "glossary.yaml"
    glossary = load_yaml(glossary_path) if glossary_path.exists() else {"terms": []}
    write_json(out / "glossary.json", glossary)
    interview_path = curriculum / "interview" / "questions.yaml"
    interview = load_yaml(interview_path) if interview_path.exists() else {"questions": []}
    write_json(out / "interview.json", interview)
    portfolio_path = curriculum / "portfolio.yaml"
    portfolio = load_yaml(portfolio_path) if portfolio_path.exists() else {"projects": []}
    write_json(out / "portfolio.json", portfolio)

    for exam in exams:
        search_items.append(
            _search_item(
                item_id=f"exam:{exam['id']}",
                kind="exam",
                title=exam["title"],
                subtitle=_truncate_i18n(exam.get("description")),
                href="/placement/" if exam["kind"] == "placement" else f"/exam/{exam['id']}/",
                tags=[t for t in (exam["kind"], exam.get("phase")) if t],
                phase=exam.get("phase"),
            )
        )
    for entry in glossary.get("terms") or []:
        term = entry["term"]
        vi_term = entry.get("vi_term")
        en = entry.get("en", "")
        vi = entry.get("vi")
        title = {"en": term}
        if vi_term and vi_term != term:
            title["vi"] = vi_term if vi_term.lower().startswith(term.lower()) else f"{term} ({vi_term})"
        search_items.append(
            _search_item(
                item_id=f"glossary:{term}",
                kind="glossary",
                title=title,
                subtitle={"en": _truncate(en, 160), **({"vi": _truncate(vi, 160)} if vi else {})},
                href=f"/glossary/?q={quote(term, safe='')}",
                tags=list(entry.get("tags") or []),
            )
        )
    for q in interview.get("questions") or []:
        iv_sub = f"{q['topic']} · {q['level']}"
        search_items.append(
            _search_item(
                item_id=f"interview:{q['id']}",
                kind="interview",
                title={
                    "en": _truncate(q["en"]["question"], 160),
                    **({"vi": _truncate(q["vi"]["question"], 160)} if q.get("vi") else {}),
                },
                subtitle={"en": iv_sub, "vi": iv_sub},
                href=f"/interview/?q={quote(q['id'], safe='')}",
                tags=[t for t in (q.get("topic"), q.get("level"), q.get("kind")) if t],
            )
        )
    for proj in portfolio.get("projects") or []:
        search_items.append(
            _search_item(
                item_id=f"portfolio:{proj['id']}",
                kind="portfolio",
                title=proj["title"],
                subtitle=_truncate_i18n(proj.get("pitch")),
                href="/portfolio/",
                tags=list(dict.fromkeys([*(proj.get("tags") or []), *(proj.get("skills") or [])])),
                phase=proj.get("phase"),
            )
        )
    write_json(out / "search.json", {"items": search_items})
    # Keep lessons/ and exams/ importable even when empty.
    (out / "lessons").mkdir(parents=True, exist_ok=True)
    (out / "exams").mkdir(parents=True, exist_ok=True)

    if web is not None:
        runner_dir = web / "public" / "pyrunner"
        runner_dir.mkdir(parents=True, exist_ok=True)
        for name in ("runner.py", "tracer.py"):
            shutil.copyfile(ROOT / "tools" / "pyrunner" / name, runner_dir / name)
        shutil.copyfile(ROOT / "packages" / "pyai_llm" / "pyai_llm.py", runner_dir / "llm.py")

    out_label = out.relative_to(ROOT) if out.is_relative_to(ROOT) else out
    print(
        f"Built {lesson_count} lessons, {len(exams)} exams, "
        f"{len(review['flashcards'])} flashcards, {len(review['questions'])} questions "
        f"-> {out_label}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
