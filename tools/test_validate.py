"""Tests for lesson validation, schemas, capstone groups, and overlap warnings."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from tools import validate


def test_expected_lines_follow_print_until_blank_or_code() -> None:
    code = (
        "x = 2\n"
        "print(x)\n"
        "# 2\n"
        "\n"
        "# explanation, not output\n"
        "print(x + 1)  # inline\n"
        "# 3\n"
        "# print(x)  # NameError: commented-out code ends the run\n"
        "# not output either\n"
    )
    assert validate.expected_output_lines(code) == [(3, "2"), (7, "3")]


def test_missing_line_in_order_and_wildcard() -> None:
    exp = [(1, "a"), (2, "<obj at 0x...>")]
    assert validate.missing_output_line(exp, "a  \n<obj at 0x7f00>\n") is None
    assert validate.missing_output_line(exp, "<obj at 0x7f00>\na\n") == (2, "<obj at 0x...>")
    assert validate.missing_output_line([(5, "b")], "a\n") == (5, "b")


def _lesson(tmp_path: Path, body: str) -> Path:
    for lang in validate.LANGS:
        md = tmp_path / f"lesson.{lang}.md"
        md.write_text(f"# T\n\n```python\n{body}```\n", encoding="utf-8")
    return tmp_path


def test_check_lesson_outputs_reports_file_block_and_line(tmp_path: Path) -> None:
    rep = validate.Report()
    validate.check_lesson_outputs(rep, _lesson(tmp_path, "print(1 + 1)\n# 3\n"))
    assert len(rep.errors) == 2  # EN and VI
    assert "lesson.en.md:5" in rep.errors[0]
    assert "python block #1" in rep.errors[0]
    assert "'3'" in rep.errors[0]


def test_check_lesson_outputs_accepts_traceback_line(tmp_path: Path) -> None:
    rep = validate.Report()
    body = "print(len(5))\n# TypeError: object of type 'int' has no len()\n"
    validate.check_lesson_outputs(rep, _lesson(tmp_path, body))
    assert rep.errors == []


def test_copied_runs() -> None:
    lesson = "```python\n" + "".join(f"x{i} = {i}\n" for i in range(6)) + "```\n"
    solution = "import os\n" + "".join(f"x{i} = {i}\n" for i in range(6)) + "y = 1\n"
    runs = validate.copied_runs(solution, lesson, min_run=5)
    assert [len(r) for _, r in runs] == [6]
    assert validate.copied_runs(solution, lesson, min_run=7) == []


def test_lesson_groups_includes_capstones() -> None:
    caps = [{"id": "cap-01-rag-chatbot", "title": {"en": "Cap", "vi": "Cap"}}]
    syllabus = {
        "phases": [{"id": "p0", "dir": "phase-00-environment", "lessons": []}],
        "capstones": caps,
    }
    groups = validate.lesson_groups(syllabus)
    assert [g["id"] for g in groups] == ["p0", "cap"]
    assert groups[1] == {"id": "cap", "dir": "capstones", "lessons": caps}
    assert validate.lesson_groups({"phases": []}) == [
        {"id": "cap", "dir": "capstones", "lessons": []}
    ]


def test_capstone_schemas_accept_valid_and_reject_invalid() -> None:
    validators = validate._validators()
    valid_meta = {
        "id": "cap-01-rag-chatbot",
        "phase": "cap",
        "order": 1,
        "kind": "project",
        "title": {"en": "Capstone", "vi": "Capstone"},
        "summary": {"en": "Summary", "vi": "Tom tat"},
        "level": "applied",
        "tags": ["rag"],
        "duration_min": 60,
        "outcomes": {"en": ["Ship"], "vi": ["Trien khai"]},
        "review_by": "2027-01-01",
    }
    assert validators["meta"].is_valid(valid_meta)
    assert not validators["meta"].is_valid({**valid_meta, "id": "cap-1-x"})
    assert not validators["meta"].is_valid({**valid_meta, "phase": "cap1"})

    valid_ex = {
        "id": "cap-01-ex01",
        "kind": "project",
        "runner": "local",
        "title": {"en": "Build", "vi": "Xay"},
        "difficulty": 3,
        "tags": ["rag"],
        "hints": {"en": ["a", "b", "c"], "vi": ["a", "b", "c"]},
    }
    assert validators["exercise"].is_valid(valid_ex)
    assert validators["exercise"].is_valid({k: v for k, v in valid_ex.items() if k != "runner"})
    assert not validators["exercise"].is_valid({**valid_ex, "runner": "remote"})
    assert not validators["exercise"].is_valid({**valid_ex, "id": "cap-1-ex01"})


def test_exercise_timeout() -> None:
    assert validate.exercise_timeout({"id": "cap-01-ex01"}) == 15
    assert validate.exercise_timeout({"id": "cap-01-ex01", "runner": "local"}) == 60
    assert validate.exercise_timeout({"id": "p6-01-ex01"}, lesson_timeout=60) == 60


def _write_yaml(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _min_questions(prefix: str) -> list[dict]:
    qs = []
    for i in range(16):
        qtype = validate.QUIZ_TYPES[i % 4]
        base = {
            "id": f"{prefix}-q{i:02d}",
            "type": qtype,
            "tags": ["rag"],
            "en": {"prompt": f"P{i}"},
            "vi": {"prompt": f"P{i}"},
        }
        if qtype == "mcq":
            base["en"]["options"] = ["A", "B"]
            base["vi"]["options"] = ["A", "B"]
            base["answer"] = 0
        elif qtype == "output":
            base["code"] = "print(1)"
            base["answer"] = "1"
        elif qtype == "fill":
            base["code"] = "x = ___"
            base["answer"] = ["1"]
        else:
            base["lines"] = ["x = 1", "print(x)"]
        qs.append(base)
    return qs


def test_validate_capstone_and_portfolio_in_tmp_curriculum(tmp_path: Path, monkeypatch) -> None:
    cur = tmp_path / "curriculum"
    _write_yaml(cur / "topics.yaml", {"topics": ["rag"]})
    _write_yaml(cur / "syllabus.yaml", {
        "phases": [{
            "id": "p0",
            "dir": "phase-00-environment",
            "order": 0,
            "icon": "terminal",
            "title": {"en": "Env", "vi": "Env"},
            "summary": {"en": "Env", "vi": "Env"},
            "lessons": [{"id": "p0-01-intro", "title": {"en": "Intro", "vi": "Intro"}}],
        }],
        "capstones": [{
            "id": "cap-01-rag-chatbot",
            "title": {"en": "Cap", "vi": "Cap"},
            "prerequisites": ["p0-01-intro"],
        }],
    })
    _write_yaml(cur / "portfolio.yaml", {
        "projects": [{
            "id": "cap-rag",
            "lesson": "cap-01-rag-chatbot",
            "phase": "p0",
            "difficulty": 1,
            "tags": ["rag"],
            "title": {"en": "Cap", "vi": "Cap"},
            "pitch": {"en": "Pitch", "vi": "Pitch"},
            "cv_bullet": {"en": "CV", "vi": "CV"},
            "skills": ["rag"],
        }],
    })

    cap_dir = cur / "capstones" / "cap-01-rag-chatbot"
    _write_yaml(cap_dir / "meta.yaml", {
        "id": "cap-01-rag-chatbot",
        "phase": "cap",
        "order": 1,
        "kind": "project",
        "title": {"en": "Cap", "vi": "Cap"},
        "summary": {"en": "Sum", "vi": "Sum"},
        "level": "applied",
        "tags": ["rag"],
        "prerequisites": ["p0-01-intro"],
        "duration_min": 60,
        "outcomes": {"en": ["Build"], "vi": ["Xay"]},
        "review_by": "2027-01-01",
    })
    for lang in ("en", "vi"):
        (cap_dir / f"lesson.{lang}.md").write_text("# Cap\n\nBody\n", encoding="utf-8")
        (cap_dir / "examples" / f"ex01.{lang}.md").parent.mkdir(parents=True, exist_ok=True)
        (cap_dir / "examples" / f"ex01.{lang}.md").write_text("# Ex\n\nExplain\n", encoding="utf-8")
    (cap_dir / "examples" / "ex01.py").write_text("print('ok')\n", encoding="utf-8")
    (cap_dir / "examples" / "ex01.out").write_text("ok\n", encoding="utf-8")

    ex_dir = cap_dir / "exercises" / "ex01-rag"
    _write_yaml(ex_dir / "exercise.yaml", {
        "id": "cap-01-ex01",
        "kind": "project",
        "runner": "local",
        "title": {"en": "Ex", "vi": "Ex"},
        "difficulty": 2,
        "tags": ["rag"],
        "hints": {"en": ["h1", "h2", "h3"], "vi": ["h1", "h2", "h3"]},
    })
    for lang in ("en", "vi"):
        (ex_dir / f"prompt.{lang}.md").write_text("# Ex\n\nPrompt\n", encoding="utf-8")
        alt_md = ex_dir / "alternatives" / f"01_alt.{lang}.md"
        alt_md.parent.mkdir(parents=True, exist_ok=True)
        alt_md.write_text("# Alt\n\nAlt\n", encoding="utf-8")
    (ex_dir / "starter.py").write_text("def f():\n    return 0\n", encoding="utf-8")
    (ex_dir / "solution.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    (ex_dir / "alternatives" / "01_alt.py").write_text(
        "def f():\n    return 2 - 1\n", encoding="utf-8"
    )
    (ex_dir / "test_exercise.py").write_text(
        "from exercise import f\n\ndef test_f():\n    assert f() == 1\n", encoding="utf-8"
    )
    _write_yaml(cap_dir / "quiz.yaml", {
        "questions": _min_questions("cap-01"),
        "flashcards": [
            {"id": f"cap-01-fc{i:02d}", "en": {"front": "F", "back": "B"},
             "vi": {"front": "F", "back": "B"}}
            for i in range(3)
        ],
    })

    monkeypatch.setattr(validate, "CURRICULUM", cur)
    monkeypatch.setattr(sys, "argv", ["validate.py", "--fast"])
    assert validate.main() == 0

    monkeypatch.setattr(sys, "argv", ["validate.py", "--fast", "--path", str(cap_dir)])
    assert validate.main() == 0
