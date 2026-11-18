"""Tests for the lesson output-comment check and the solution overlap warning."""

from __future__ import annotations

from pathlib import Path

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
