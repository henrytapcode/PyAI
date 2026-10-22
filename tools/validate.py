"""Automated quality gate for curriculum/.

Checks (see docs/DESIGN.md section 9, step 4):
  * JSON Schema for meta.yaml, exercise.yaml, quiz.yaml, exams, glossary, interview bank
  * IDs are unique, lessons are listed in syllabus.yaml, prerequisites and tags exist
  * VI/EN parity: both files/fields exist, same structure, same code (comments may differ)
  * examples run and print exactly their .out file, have an EN+VI explanation, and the
    step-through tracer (tools/pyrunner/tracer.py) handles them
  * every exercise: starter FAILS and solution PASSES, both with pytest and with the
    browser test runner (tools/pyrunner/runner.py) so the web app grades identically;
    every alternative solution (exercises/*/alternatives/*.py) passes too
  * lesson quizzes: question bank size and type mix (the app draws a shuffled subset per attempt)
  * quiz code: "output" answers are correct, "fill" answers and "parsons" orders run
  * ruff on curriculum code

Usage:
  uv run python tools/validate.py                 # everything
  uv run python tools/validate.py --path curriculum/phase-01-python-core/p1-01-variables
  uv run python tools/validate.py --fast          # skip pytest subprocesses and ruff
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys
import tokenize
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM = ROOT / "curriculum"
SCHEMA_DIR = ROOT / "tools" / "schema"
sys.path.insert(0, str(ROOT / "tools" / "pyrunner"))
from runner import run_tests  # noqa: E402
from tracer import trace  # noqa: E402

LANGS = ("en", "vi")
QUIZ_MIN_QUESTIONS = 15
QUIZ_TYPES = ("mcq", "output", "fill", "parsons")
# Options that stop making sense once the app shuffles them.
POSITIONAL_OPTION = re.compile(r"(all|none|both) of the (above|these)|^both [a-d] and|cả hai|tất cả các (đáp án|phương án) trên", re.I)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked: dict[str, int] = field(default_factory=dict)

    def error(self, where: Path | str, msg: str) -> None:
        self.errors.append(f"{_rel(where)}: {msg}")

    def warn(self, where: Path | str, msg: str) -> None:
        self.warnings.append(f"{_rel(where)}: {msg}")

    def count(self, key: str, n: int = 1) -> None:
        self.checked[key] = self.checked.get(key, 0) + n


def _rel(p: Path | str) -> str:
    try:
        return str(Path(p).resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


# ------------------------------------------------------------------ schemas
def _validators() -> dict[str, Draft202012Validator]:
    resources = {}
    for p in SCHEMA_DIR.glob("*.schema.json"):
        schema = json.loads(p.read_text(encoding="utf-8"))
        resources[schema["$id"]] = DRAFT202012.create_resource(schema)
    registry = Registry().with_resources(resources.items())
    return {
        name: Draft202012Validator(resources[f"{name}.schema.json"].contents, registry=registry)
        for name in ("meta", "exercise", "quiz", "exam", "glossary", "interview", "portfolio")
    }


def check_schema(rep: Report, validator: Draft202012Validator, data, path: Path) -> bool:
    ok = True
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        loc = "/".join(str(x) for x in err.path) or "<root>"
        rep.error(path, f"schema: {loc}: {err.message}")
        ok = False
    return ok


# ------------------------------------------------------------------ parity helpers
def code_tokens(src: str) -> list[str] | None:
    """Tokens of Python code without comments, so translated comments are allowed."""
    try:
        toks = tokenize.generate_tokens(io.StringIO(src).readline)
        return [t.string for t in toks if t.type not in (tokenize.COMMENT, tokenize.NL)]
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return None


FENCE = re.compile(r"```(\w*)[^\n]*\n(.*?)```", re.S)


def md_structure(text: str) -> dict:
    blocks = FENCE.findall(text)
    no_code = FENCE.sub("", text)
    return {
        "headings": len(re.findall(r"^#{1,6} ", no_code, re.M)),
        "callouts": re.findall(r"^> \[!(\w+)\]", no_code, re.M),
        "code": blocks,
    }


def check_md_parity(rep: Report, en_path: Path, vi_path: Path, allow_missing_vi: bool) -> None:
    if not en_path.exists():
        rep.error(en_path, "missing English file")
        return
    if not vi_path.exists():
        (rep.warn if allow_missing_vi else rep.error)(vi_path, "missing Vietnamese translation")
        return
    en, vi = md_structure(en_path.read_text("utf-8")), md_structure(vi_path.read_text("utf-8"))
    if en["headings"] != vi["headings"]:
        rep.error(vi_path, f"parity: {vi['headings']} headings vs {en['headings']} in EN")
    if en["callouts"] != vi["callouts"]:
        rep.error(vi_path, f"parity: callouts {vi['callouts']} vs {en['callouts']} in EN")
    if len(en["code"]) != len(vi["code"]):
        rep.error(vi_path, f"parity: {len(vi['code'])} code blocks vs {len(en['code'])} in EN")
        return
    for i, ((lang_en, c_en), (lang_vi, c_vi)) in enumerate(zip(en["code"], vi["code"]), 1):
        if lang_en in ("python", "py"):
            same = code_tokens(c_en) == code_tokens(c_vi)
        elif lang_en == "mermaid":
            # Diagram labels are translated; the diagram shape must match.
            same = lang_vi == "mermaid" and len(c_en.strip().splitlines()) == len(c_vi.strip().splitlines())
        else:
            same = c_en.strip() == c_vi.strip()
        if not same:
            rep.error(vi_path, f"parity: code block #{i} differs from EN (only comments may be translated)")
    rep.count("markdown pairs")


def check_i18n_obj(rep: Report, path: Path, obj, where: str, allow_missing_vi: bool) -> None:
    """Recursively find {en: ..., vi: ...} objects and compare their shape."""
    if isinstance(obj, dict):
        if "en" in obj:
            en, vi = obj.get("en"), obj.get("vi")
            if vi is None:
                (rep.warn if allow_missing_vi else rep.error)(path, f"{where}: missing 'vi'")
            elif isinstance(en, list) and (not isinstance(vi, list) or len(en) != len(vi)):
                rep.error(path, f"{where}: 'vi' list length differs from 'en'")
            elif isinstance(en, dict) and isinstance(vi, dict):
                if set(en) != set(vi):
                    rep.error(path, f"{where}: vi fields {sorted(vi)} != en fields {sorted(en)}")
                for k in en:
                    if isinstance(en[k], list) and len(en[k]) != len(vi.get(k) or []):
                        rep.error(path, f"{where}.{k}: vi has {len(vi.get(k) or [])} items, en has {len(en[k])}")
        for k, v in obj.items():
            if k not in LANGS:
                check_i18n_obj(rep, path, v, f"{where}.{k}" if where else k, allow_missing_vi)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            label = v.get("id", i) if isinstance(v, dict) else i
            check_i18n_obj(rep, path, v, f"{where}[{label}]", allow_missing_vi)


# ------------------------------------------------------------------ running code
def run_python(code: str, cwd: Path | None = None, timeout: int = 15) -> tuple[int, str, str]:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    proc = subprocess.run(
        [sys.executable, "-I", "-c", code], capture_output=True, text=True,
        encoding="utf-8", timeout=timeout, cwd=cwd, env=env,
    )
    return proc.returncode, proc.stdout, proc.stderr


def norm_out(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def md_title(path: Path) -> str | None:
    first = path.read_text("utf-8").lstrip().splitlines()[0] if path.exists() else ""
    return first[2:].strip() if first.startswith("# ") else None


def check_explained_code(rep: Report, py: Path, args, what: str) -> None:
    """A code file with ``<stem>.en.md`` / ``<stem>.vi.md`` next to it: '# Title' then the explanation."""
    en, vi = py.with_suffix(".en.md"), py.with_suffix(".vi.md")
    if not en.exists():
        rep.error(py, f"{what} needs an explanation file {en.name} ('# Title' + explanation)")
        return
    for f in (en, vi):
        if f.exists() and not md_title(f):
            rep.error(f, "must start with a '# Title' line")
    check_md_parity(rep, en, vi, args.allow_missing_vi)


def check_examples(rep: Report, lesson_dir: Path, args) -> None:
    ex_dir = lesson_dir / "examples"
    if not ex_dir.exists():
        rep.error(lesson_dir, "missing examples/ folder")
        return
    files = sorted(ex_dir.glob("*.py"))
    if not files:
        rep.error(ex_dir, "no example .py files")
    for py in files:
        out_file = py.with_suffix(".out")
        code, out, err = run_python(py.read_text("utf-8"), cwd=ex_dir)
        if code != 0:
            rep.error(py, f"example crashed:\n{err.strip()[-600:]}")
        elif not out_file.exists():
            rep.error(out_file, "missing expected output (.out)")
        elif norm_out(out) != norm_out(out_file.read_text("utf-8")):
            rep.error(py, f"output differs from {out_file.name}:\n--- got ---\n{out}--- expected ---\n{out_file.read_text('utf-8')}")
        check_explained_code(rep, py, args, "example")
        if code == 0:
            traced = trace(py.read_text("utf-8"))
            if traced["error"]:
                rep.error(py, f"step-through tracer fails: {traced['error']}")
        rep.count("examples")


def check_exercise(rep: Report, ex_dir: Path, validators, ids: set, topics: set, args) -> None:
    meta_path = ex_dir / "exercise.yaml"
    if not meta_path.exists():
        rep.error(ex_dir, "missing exercise.yaml")
        return
    meta = load_yaml(meta_path)
    if check_schema(rep, validators["exercise"], meta, meta_path):
        _unique(rep, ids, meta["id"], meta_path)
        _check_tags(rep, meta_path, meta["tags"], topics)
    check_i18n_obj(rep, meta_path, meta, "", args.allow_missing_vi)
    check_md_parity(rep, ex_dir / "prompt.en.md", ex_dir / "prompt.vi.md", args.allow_missing_vi)
    files = {n: ex_dir / f"{n}.py" for n in ("starter", "solution", "test_exercise")}
    for name, p in files.items():
        if not p.exists():
            rep.error(p, f"missing {p.name}")
            return
    test_src = files["test_exercise"].read_text("utf-8")
    starter = run_tests(files["starter"].read_text("utf-8"), test_src)
    solution = run_tests(files["solution"].read_text("utf-8"), test_src)
    if starter["ok"]:
        rep.error(files["starter"], "browser runner: starter PASSES all tests (it must fail)")
    if not solution["ok"]:
        failing = [t for t in solution["tests"] if t["status"] != "passed"]
        detail = solution["error"] or (failing[0] if failing else "no tests collected")
        rep.error(files["solution"], f"browser runner: solution does not pass: {detail}")
    if meta.get("kind") == "fill" and "___" not in files["starter"].read_text("utf-8"):
        rep.error(files["starter"], "kind 'fill' but starter has no ___ blanks")
    alt_dir = ex_dir / "alternatives"
    alts = sorted(alt_dir.glob("*.py")) if alt_dir.exists() else []
    if not alts and meta.get("kind") in ("code", "project"):
        rep.error(ex_dir, "kind 'code'/'project' needs at least one alternatives/NN_name.py (+ .en.md/.vi.md)")
    for alt in alts:
        res = run_tests(alt.read_text("utf-8"), test_src)
        if not res["ok"]:
            failing = [t for t in res["tests"] if t["status"] != "passed"]
            rep.error(alt, f"alternative solution does not pass: {res['error'] or (failing[0] if failing else 'no tests')}")
        if alt.read_text("utf-8").strip() == files["solution"].read_text("utf-8").strip():
            rep.error(alt, "alternative is identical to solution.py")
        check_explained_code(rep, alt, args, "alternative solution")
        rep.count("alternatives")
    if not args.fast:
        for target, should_pass in (("starter", False), ("solution", True)):
            env = dict(os.environ, EXERCISE_TARGET=target, PYTHONUTF8="1")
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--rootdir", str(CURRICULUM),
                 str(files["test_exercise"])],
                capture_output=True, text=True, encoding="utf-8", env=env, cwd=ROOT, timeout=120,
            )
            passed = proc.returncode == 0
            if passed != should_pass:
                verdict = "passes" if passed else "fails"
                rep.error(files[target], f"pytest: {target} {verdict} (expected {'pass' if should_pass else 'fail'})\n{proc.stdout[-800:]}")
    rep.count("exercises")


def _unique(rep: Report, ids: set, id_: str, where: Path) -> None:
    if id_ in ids:
        rep.error(where, f"duplicate id '{id_}'")
    ids.add(id_)


def _check_tags(rep: Report, where: Path, tags, topics: set) -> None:
    for t in tags or []:
        if t not in topics:
            rep.error(where, f"unknown tag '{t}' (add it to curriculum/topics.yaml)")


def check_questions(rep: Report, path: Path, questions: list, ids: set, topics: set) -> None:
    for q in questions:
        qid = q.get("id", "?")
        _unique(rep, ids, qid, path)
        _check_tags(rep, path, q.get("tags"), topics)
        for lang in LANGS:
            t = q.get(lang) or {}
            if q["type"] == "mcq":
                opts = t.get("options") or []
                if len(opts) < 2:
                    rep.error(path, f"{qid}: mcq needs options in '{lang}'")
                elif not 0 <= q.get("answer", -1) < len(opts):
                    rep.error(path, f"{qid}: answer index out of range in '{lang}'")
                if q.get("shuffle_options", True) and any(POSITIONAL_OPTION.search(o) for o in opts):
                    rep.error(path, f"{qid}: option refers to other options; set shuffle_options: false or reword")
                if len(set(opts)) != len(opts):
                    rep.error(path, f"{qid}: duplicate options in '{lang}'")
        code = q.get("code", "")
        if q["type"] == "output":
            rc, out, err = run_python(code)
            if rc != 0:
                rep.error(path, f"{qid}: code crashes: {err.strip()[-300:]}")
            elif norm_out(out) != norm_out(q["answer"]):
                rep.error(path, f"{qid}: answer {q['answer']!r} but code prints {out.strip()!r}")
        elif q["type"] == "fill":
            blanks = code.count("___")
            if blanks != len(q["answer"]):
                rep.error(path, f"{qid}: {blanks} blanks but {len(q['answer'])} answers")
            else:
                filled = code
                for a in q["answer"]:
                    first = a[0] if isinstance(a, list) else a
                    filled = filled.replace("___", first, 1)
                rc, _, err = run_python(filled)
                if rc != 0:
                    rep.error(path, f"{qid}: code with answers filled in crashes: {err.strip()[-300:]}")
        elif q["type"] == "parsons":
            rc, _, err = run_python("\n".join(q["lines"]) + "\n")
            if rc != 0:
                rep.error(path, f"{qid}: parsons lines in given order crash: {err.strip()[-300:]}")
            if len(set(q["lines"])) != len(q["lines"]):
                rep.error(path, f"{qid}: parsons lines must be unique")
        rep.count("questions")


# ------------------------------------------------------------------ main walk
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--path", type=Path, help="only check this lesson folder (or any folder below curriculum/)")
    ap.add_argument("--fast", action="store_true", help="skip pytest subprocesses and ruff")
    ap.add_argument("--allow-missing-vi", action="store_true", help="missing translations become warnings")
    args = ap.parse_args()

    rep = Report()
    validators = _validators()
    syllabus = load_yaml(CURRICULUM / "syllabus.yaml")
    topics = set(load_yaml(CURRICULUM / "topics.yaml")["topics"])
    lesson_index = {les["id"]: (ph, les) for ph in syllabus["phases"] for les in ph["lessons"]}
    check_i18n_obj(rep, CURRICULUM / "syllabus.yaml", syllabus, "", args.allow_missing_vi)
    for lid, (_, les) in lesson_index.items():
        for pre in les.get("prerequisites", []):
            if pre not in lesson_index:
                rep.error(CURRICULUM / "syllabus.yaml", f"{lid}: unknown prerequisite '{pre}'")

    scope = (args.path.resolve() if args.path else CURRICULUM)
    ids: set[str] = set()

    for phase in syllabus["phases"]:
        phase_dir = CURRICULUM / phase["dir"]
        if not phase_dir.exists():
            continue
        for lesson_dir in sorted(p for p in phase_dir.iterdir() if p.is_dir() and (p / "meta.yaml").exists()):
            in_scope = scope in (lesson_dir, *lesson_dir.parents) or lesson_dir in scope.parents
            meta_path = lesson_dir / "meta.yaml"
            meta = load_yaml(meta_path)
            if check_schema(rep, validators["meta"], meta, meta_path):
                _unique(rep, ids, meta["id"], meta_path)
                _check_tags(rep, meta_path, meta["tags"], topics)
                if meta["id"] != lesson_dir.name:
                    rep.error(meta_path, f"id '{meta['id']}' must equal folder name '{lesson_dir.name}'")
                if meta["id"] not in lesson_index:
                    rep.error(meta_path, f"lesson '{meta['id']}' is not listed in syllabus.yaml")
                elif lesson_index[meta["id"]][0]["id"] != meta["phase"]:
                    rep.error(meta_path, f"phase '{meta['phase']}' does not match syllabus")
                for pre in meta.get("prerequisites", []):
                    if pre not in lesson_index:
                        rep.error(meta_path, f"unknown prerequisite '{pre}'")
            if not in_scope:
                continue
            rep.count("lessons")
            check_i18n_obj(rep, meta_path, meta, "", args.allow_missing_vi)
            check_md_parity(rep, lesson_dir / "lesson.en.md", lesson_dir / "lesson.vi.md", args.allow_missing_vi)
            check_examples(rep, lesson_dir, args)
            ex_root = lesson_dir / "exercises"
            ex_dirs = sorted(p for p in ex_root.iterdir() if p.is_dir()) if ex_root.exists() else []
            if not ex_dirs:
                rep.error(lesson_dir, "lesson has no exercises")
            for ex_dir in ex_dirs:
                check_exercise(rep, ex_dir, validators, ids, topics, args)
            quiz_path = lesson_dir / "quiz.yaml"
            if not quiz_path.exists():
                rep.error(lesson_dir, "missing quiz.yaml")
            else:
                quiz = load_yaml(quiz_path)
                if check_schema(rep, validators["quiz"], quiz, quiz_path):
                    check_questions(rep, quiz_path, quiz["questions"], ids, topics)
                    qs = quiz["questions"]
                    if len(qs) < QUIZ_MIN_QUESTIONS:
                        rep.error(quiz_path, f"question bank has {len(qs)} questions, needs >= {QUIZ_MIN_QUESTIONS}")
                    missing = [t for t in QUIZ_TYPES if sum(q["type"] == t for q in qs) < 2]
                    if missing:
                        rep.error(quiz_path, f"needs at least 2 questions of each type, short on: {missing}")
                    for card in quiz["flashcards"]:
                        _unique(rep, ids, card["id"], quiz_path)
                        _check_tags(rep, quiz_path, card.get("tags"), topics)
                check_i18n_obj(rep, quiz_path, quiz, "", args.allow_missing_vi)

    # Exams, placement, phase tests
    for exam_path in sorted(CURRICULUM.rglob("*.yaml")):
        if exam_path.parent.name == "exams" or exam_path.name in ("phase-test.yaml", "placement.yaml"):
            if not (scope in (exam_path, *exam_path.parents)):
                continue
            exam = load_yaml(exam_path)
            if check_schema(rep, validators["exam"], exam, exam_path):
                _unique(rep, ids, exam["id"], exam_path)
                check_questions(rep, exam_path, exam["questions"], ids, topics)
            check_i18n_obj(rep, exam_path, exam, "", args.allow_missing_vi)
            rep.count("exams")

    if scope == CURRICULUM:
        portfolio_path = CURRICULUM / "portfolio.yaml"
        if portfolio_path.exists():
            portfolio = load_yaml(portfolio_path)
            if check_schema(rep, validators["portfolio"], portfolio, portfolio_path):
                check_i18n_obj(rep, portfolio_path, portfolio["projects"], "", args.allow_missing_vi)
                diffs = [pr["difficulty"] for pr in portfolio["projects"]]
                if diffs != sorted(diffs):
                    rep.error(portfolio_path, "projects must be listed by increasing difficulty")
                for pr in portfolio["projects"]:
                    if pr.get("lesson") and pr["lesson"] not in lesson_index:
                        rep.error(portfolio_path, f"{pr['id']}: unknown lesson '{pr['lesson']}'")
                    _check_tags(rep, portfolio_path, pr.get("tags"), topics)
                rep.count("portfolio")
        for name, key in (("glossary.yaml", "glossary"), ("interview/questions.yaml", "interview")):
            p = CURRICULUM / name
            if p.exists():
                data = load_yaml(p)
                check_schema(rep, validators[key], data, p)
                check_i18n_obj(rep, p, data.get("terms") or data.get("questions"), "", args.allow_missing_vi)
                if key == "glossary":
                    seen: set[str] = set()
                    for t in data.get("terms", []):
                        if "vi" not in t:
                            (rep.warn if args.allow_missing_vi else rep.error)(p, f"term '{t['term']}' missing 'vi'")
                        if t["term"].lower() in seen:
                            rep.error(p, f"duplicate glossary term '{t['term']}'")
                        seen.add(t["term"].lower())
                        _check_tags(rep, p, t.get("tags"), topics)
                else:
                    for q in data.get("questions", []):
                        _unique(rep, ids, q["id"], p)
                        _check_tags(rep, p, [q["topic"]], topics)
                rep.count(key)

    if not args.fast:
        proc = subprocess.run(
            [sys.executable, "-m", "ruff", "check", "--quiet", str(scope)],
            capture_output=True, text=True, encoding="utf-8", cwd=ROOT,
        )
        if proc.returncode != 0:
            rep.error("ruff", proc.stdout.strip() or proc.stderr.strip())

    for w in rep.warnings:
        print(f"WARN  {w}")
    for e in rep.errors:
        print(f"ERROR {e}")
    summary = ", ".join(f"{v} {k}" for k, v in rep.checked.items())
    status = "FAILED" if rep.errors else "OK"
    print(f"\n{status}: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s). Checked {summary}.")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
