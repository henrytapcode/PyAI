"""Unit and integration tests for tools/export_pdf.py."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from tools import export_pdf


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def _make_synthetic_generated(root: Path) -> Path:
    gen = root / "generated"
    catalog = {
        "phases": [
            {
                "id": "p0",
                "order": 0,
                "title": {"en": "Setup", "vi": "Cài đặt"},
                "summary": {"en": "Env setup", "vi": "Thiết lập"},
                "lessons": [
                    {
                        "id": "p0-01-setup",
                        "order": 1,
                        "kind": "lesson",
                        "title": {"en": "Hidden P0", "vi": "P0 ẩn"},
                        "outcomes": {"en": ["Not ready"], "vi": ["Chưa sẵn sàng"]},
                        "ready": False,
                    }
                ],
            },
            {
                "id": "p1",
                "order": 1,
                "title": {"en": "Python Core", "vi": "Python cốt lõi"},
                "summary": {"en": "Core syntax.", "vi": "Cú pháp cốt lõi."},
                "lessons": [
                    {
                        "id": "p1-01-vars",
                        "order": 1,
                        "kind": "lesson",
                        "title": {"en": "Variables", "vi": "Biến"},
                        "outcomes": {"en": ["Use variables"], "vi": ["Dùng biến"]},
                        "ready": True,
                    }
                ],
            },
        ],
        "capstones": [
            {
                "id": "cap-01-demo",
                "order": 1,
                "kind": "project",
                "title": {"en": "Capstone Demo", "vi": "Capstone mẫu"},
                "outcomes": {"en": ["Build agent"], "vi": ["Xây agent"]},
                "ready": True,
            }
        ],
        "exams": [
            {
                "id": "mock-mini",
                "kind": "mock",
                "title": {"en": "Mini Mock", "vi": "Thi thử nhỏ"},
                "description": {"en": "Sample exam.", "vi": "Đề thi mẫu."},
                "duration_min": 20,
                "pass_score": 0.8,
                "questionCount": 4,
            }
        ],
    }
    _write_json(gen / "catalog.json", catalog)

    _write_json(
        gen / "lessons" / "p1-01-vars.json",
        {
            "meta": {
                "id": "p1-01-vars",
                "duration_min": 10,
                "title": {"en": "Variables", "vi": "Biến"},
                "summary": {"en": "Intro vars", "vi": "Giới thiệu biến"},
                "outcomes": {"en": ["Use variables"], "vi": ["Dùng biến"]},
            },
            "body": {
                "en": "# Intro\n\nAssign `x = 1`.\n\n## Recap\n\n- Variables store values.\n",
                "vi": "# Mở đầu\n\nGán `x = 1`.\n\n## Tóm tắt\n\n- Biến lưu trữ giá trị.\n",
            },
            "examples": [
                {
                    "name": "01_vars",
                    "title": {"en": "Assign", "vi": "Gán biến"},
                    "code": "x = 1\nprint(x)",
                    "output": "1",
                }
            ],
            "exercises": [
                {
                    "id": "p1-01-ex01",
                    "title": {"en": "Ex 1", "vi": "Bài 1"},
                    "prompt": {"en": "Set `y = 2`.", "vi": "Đặt `y = 2`."},
                    "solution": "SECRET_SOLUTION_TOKEN = 42",
                }
            ],
            "quiz": {
                "flashcards": [
                    {
                        "id": "f1",
                        "en": {"front": "Variable", "back": "Named reference"},
                        "vi": {"front": "Biến", "back": "Tên tham chiếu"},
                    }
                ]
            },
        },
    )

    _write_json(
        gen / "lessons" / "cap-01-demo.json",
        {
            "meta": {
                "id": "cap-01-demo",
                "duration_min": 60,
                "title": {"en": "Capstone Demo", "vi": "Capstone mẫu"},
                "summary": {"en": "Capstone summary.", "vi": "Tóm tắt capstone."},
                "outcomes": {"en": ["Build agent"], "vi": ["Xây agent"]},
            },
            "body": {
                "en": "## Architecture\n\nRun tools.\n\n## Recap\n\n- Scope tools.\n",
                "vi": "## Kiến trúc\n\nChạy tool.\n\n## Tóm tắt\n\n- Phân quyền tool.\n",
            },
            "examples": [],
            "exercises": [],
            "quiz": {"flashcards": []},
        },
    )

    _write_json(
        gen / "exams" / "mock-mini.json",
        {
            "id": "mock-mini",
            "kind": "mock",
            "title": {"en": "Mini Mock", "vi": "Thi thử nhỏ"},
            "description": {"en": "Sample exam.", "vi": "Đề thi mẫu."},
            "duration_min": 20,
            "pass_score": 0.8,
            "questions": [
                {
                    "id": "q1",
                    "type": "mcq",
                    "answer": 1,
                    "en": {
                        "prompt": "Pick the valid keyword.",
                        "options": ["func", "def", "define", "fn"],
                        "explanation": "SECRET_MCQ_EXPL: Python uses def.",
                    },
                    "vi": {
                        "prompt": "Chọn từ khóa đúng.",
                        "options": ["func", "def", "define", "fn"],
                        "explanation": "SECRET_MCQ_EXPL_VI: Python dùng def.",
                    },
                },
                {
                    "id": "q2",
                    "type": "output",
                    "code": "print(2 + 3)",
                    "answer": "SECRET_STDOUT_5",
                    "en": {"prompt": "What does it print?", "explanation": "EXPL_Q2"},
                    "vi": {"prompt": "In ra gì?", "explanation": "EXPL_Q2_VI"},
                },
                {
                    "id": "q3",
                    "type": "fill",
                    "code": "x = ___(42)",
                    "answer": ["SECRET_STR_FILL"],
                    "en": {"prompt": "Fill in.", "explanation": "EXPL_Q3"},
                    "vi": {"prompt": "Điền vào.", "explanation": "EXPL_Q3_VI"},
                },
                {
                    "id": "q4",
                    "type": "parsons",
                    "lines": ["def f():", "    x = 1", "    return x"],
                    "answer": [0, 1, 2],
                    "en": {"prompt": "Order lines.", "explanation": "EXPL_Q4"},
                    "vi": {"prompt": "Sắp xếp dòng.", "explanation": "EXPL_Q4_VI"},
                },
            ],
        },
    )
    return gen


def test_render_markdown_elements_and_escaping() -> None:
    md = (
        "# Title <script>alert(1)</script>\n\n"
        "Text with **bold**, *italic*, `code`, and [link](https://example.com).\n\n"
        "> [!WARNING] Watch out!\n\n"
        "| col1 | col2 |\n|---|---|\n| a | b |\n\n"
        "```mermaid\nflowchart LR\n  A --> B\n```\n"
    )
    rendered = export_pdf.render_markdown(md)
    assert "<h1>Title &lt;script&gt;alert(1)&lt;/script&gt;</h1>" in rendered
    assert "<strong>bold</strong>" in rendered
    assert "<em>italic</em>" in rendered
    assert "<code>code</code>" in rendered
    assert '<a href="https://example.com">link</a>' in rendered
    assert 'class="callout warning"' in rendered
    assert "<table><thead><tr><th>col1</th><th>col2</th></tr></thead>" in rendered
    assert '<pre class="mermaid-src"><code>flowchart LR' in rendered


def test_find_browser(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    fake = tmp_path / "chrome.exe"
    fake.write_text("bin", encoding="utf-8")
    assert export_pdf.find_browser(str(fake)) == fake
    assert export_pdf.find_browser(str(tmp_path / "missing.exe")) is None

    monkeypatch.setattr(
        export_pdf.shutil,
        "which",
        lambda name: str(fake) if name == "msedge" else None,
    )
    assert export_pdf.find_browser() == fake


def test_html_to_pdf_mocked(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    html_file = tmp_path / "doc.html"
    pdf_file = tmp_path / "out" / "doc.pdf"
    browser = tmp_path / "chrome.exe"
    html_file.write_text("<html><body>hi</body></html>", encoding="utf-8")
    browser.write_text("bin", encoding="utf-8")

    def fake_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[bytes]:
        assert "--headless" in cmd
        assert any(arg.startswith("--print-to-pdf=") for arg in cmd)
        pdf_file.write_bytes(b"%PDF-1.4\n%fake\n")
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(export_pdf.subprocess, "run", fake_run)
    res = export_pdf.html_to_pdf(html_file, pdf_file, browser)
    assert res == pdf_file.resolve()
    assert res.read_bytes().startswith(b"%PDF-")


def test_html_to_pdf_raises_on_empty_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    html_file = tmp_path / "doc.html"
    pdf_file = tmp_path / "doc.pdf"
    browser = tmp_path / "chrome.exe"
    html_file.write_text("<html></html>", encoding="utf-8")
    browser.write_text("bin", encoding="utf-8")

    monkeypatch.setattr(
        export_pdf.subprocess,
        "run",
        lambda cmd, **kwargs: subprocess.CompletedProcess(cmd, 0),
    )
    with pytest.raises(RuntimeError, match="non-empty PDF"):
        export_pdf.html_to_pdf(html_file, pdf_file, browser)


def test_missing_catalog_raises_actionable_error(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="build_content.py"):
        export_pdf.build_textbook_html(tmp_path, "en")


def test_build_textbook_skips_unready_and_excludes_solutions(tmp_path: Path) -> None:
    gen = _make_synthetic_generated(tmp_path)
    doc = export_pdf.build_textbook_html(gen, "en")
    assert "Hidden P0" not in doc
    assert "Variables" in doc
    assert "Capstone Demo" in doc
    assert "Use variables" in doc
    assert "Set <code>y = 2</code>." in doc
    assert "SECRET_SOLUTION_TOKEN" not in doc


def test_build_cheatsheet_html_and_unknown_phase(tmp_path: Path) -> None:
    gen = _make_synthetic_generated(tmp_path)
    p1_vi = export_pdf.build_cheatsheet_html(gen, "p1", "vi")
    assert "Python cốt lõi" in p1_vi
    assert "Biến lưu trữ giá trị." in p1_vi
    assert "Tên tham chiếu" in p1_vi

    cap_en = export_pdf.build_cheatsheet_html(gen, "cap", "en")
    assert "Scope tools." in cap_en

    with pytest.raises(ValueError, match="Unknown phase_id"):
        export_pdf.build_cheatsheet_html(gen, "p99", "en")


def test_exam_sheet_zero_leak_and_parsons_shuffle(tmp_path: Path) -> None:
    gen = _make_synthetic_generated(tmp_path)
    exam = json.loads((gen / "exams" / "mock-mini.json").read_text(encoding="utf-8"))

    sheet = export_pdf.build_exam_sheet_html(exam, "en")
    assert "SECRET_MCQ_EXPL" not in sheet
    assert "SECRET_STDOUT_5" not in sheet
    assert "SECRET_STR_FILL" not in sheet
    assert "EXPL_Q2" not in sheet
    assert "<strong>B.</strong> def" in sheet

    canonical = "1. def f():\n2.     x = 1\n3.     return x"
    assert canonical not in sheet

    answers = export_pdf.build_exam_answers_html(exam, "en")
    assert "B. def" in answers
    assert "SECRET_MCQ_EXPL" in answers
    assert "SECRET_STDOUT_5" in answers
    assert "SECRET_STR_FILL" in answers
    assert "EXPL_Q4" in answers


def test_export_all_html_only(tmp_path: Path) -> None:
    gen = _make_synthetic_generated(tmp_path)
    out = tmp_path / "exports"
    res = export_pdf.export_all(gen, out, only="all", lang="both", html_only=True)
    assert res["pdf"] == []
    stems = {p.stem for p in res["html"]}
    assert "pyai-textbook-en" in stems
    assert "pyai-textbook-vi" in stems
    assert "cheatsheet-p1-en" in stems
    assert "cheatsheet-cap-vi" in stems
    assert "exam-mock-mini-en" in stems
    assert "exam-mock-mini-en-answers" in stems


def test_integration_real_generated_if_present(tmp_path: Path) -> None:
    real_gen = Path("apps/web/src/generated")
    if not (real_gen / "catalog.json").exists():
        pytest.skip("generated content not built")
    res = export_pdf.export_all(
        real_gen,
        tmp_path / "exports",
        only="sheets",
        lang="en",
        phase_id="cap",
        html_only=True,
    )
    assert len(res["html"]) == 1
    text = res["html"][0].read_text(encoding="utf-8")
    assert "Capstone: tool-using agent" in text
