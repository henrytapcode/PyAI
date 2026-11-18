"""Tests for tools/build_content.py capstone support."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from tools import build_content


def _write_yaml(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def test_build_content_with_ready_and_unbuilt_capstones(tmp_path: Path) -> None:
    cur = tmp_path / "curriculum"
    out = tmp_path / "out"
    _write_yaml(cur / "topics.yaml", {"topics": ["python", "rag"]})
    _write_yaml(
        cur / "syllabus.yaml",
        {
            "phases": [
                {
                    "id": "p0",
                    "dir": "phase-00-environment",
                    "order": 0,
                    "icon": "terminal",
                    "title": {"en": "Env", "vi": "Env"},
                    "summary": {"en": "Env", "vi": "Env"},
                    "lessons": [{"id": "p0-01-intro", "title": {"en": "Intro", "vi": "Intro"}}],
                }
            ],
            "capstones": [
                {
                    "id": "cap-01-rag-chatbot",
                    "kind": "project",
                    "runner": "local",
                    "title": {"en": "RAG Cap", "vi": "RAG Cap"},
                    "prerequisites": ["p0-01-intro"],
                },
                {
                    "id": "cap-02-tool-agent",
                    "title": {"en": "Agent Cap", "vi": "Agent Cap"},
                    "prerequisites": ["p0-01-intro"],
                },
            ],
        },
    )

    p0_dir = cur / "phase-00-environment" / "p0-01-intro"
    _write_yaml(
        p0_dir / "meta.yaml",
        {
            "id": "p0-01-intro",
            "phase": "p0",
            "order": 1,
            "title": {"en": "Intro", "vi": "Intro"},
            "summary": {"en": "Intro", "vi": "Intro"},
            "level": "beginner",
            "tags": ["python"],
            "duration_min": 10,
            "outcomes": {"en": ["Run"], "vi": ["Chay"]},
            "review_by": "2027-01-01",
        },
    )
    (p0_dir / "lesson.en.md").write_text("# Intro\n", encoding="utf-8")
    (p0_dir / "lesson.vi.md").write_text("# Intro\n", encoding="utf-8")

    cap_dir = cur / "capstones" / "cap-01-rag-chatbot"
    _write_yaml(
        cap_dir / "meta.yaml",
        {
            "id": "cap-01-rag-chatbot",
            "phase": "cap",
            "order": 1,
            "kind": "project",
            "title": {"en": "RAG Cap", "vi": "RAG Cap"},
            "summary": {"en": "Build RAG", "vi": "Xay RAG"},
            "level": "applied",
            "tags": ["rag"],
            "prerequisites": ["p0-01-intro"],
            "duration_min": 60,
            "outcomes": {"en": ["Ship"], "vi": ["Trien khai"]},
            "review_by": "2027-01-01",
        },
    )
    (cap_dir / "lesson.en.md").write_text("# Cap\n", encoding="utf-8")
    (cap_dir / "lesson.vi.md").write_text("# Cap\n", encoding="utf-8")

    ex_dir = cap_dir / "exercises" / "ex01-rag"
    _write_yaml(
        ex_dir / "exercise.yaml",
        {
            "id": "cap-01-ex01",
            "kind": "project",
            "runner": "local",
            "title": {"en": "Ex", "vi": "Ex"},
            "difficulty": 2,
            "tags": ["rag"],
            "hints": {"en": ["a", "b", "c"], "vi": ["a", "b", "c"]},
        },
    )
    (ex_dir / "prompt.en.md").write_text("Prompt", encoding="utf-8")
    (ex_dir / "prompt.vi.md").write_text("Prompt", encoding="utf-8")
    (ex_dir / "starter.py").write_text("def f():\n    return 0\n", encoding="utf-8")
    (ex_dir / "solution.py").write_text("def f():\n    return 1\n", encoding="utf-8")
    (ex_dir / "test_exercise.py").write_text("def test_f():\n    assert True\n", encoding="utf-8")

    _write_yaml(
        cap_dir / "quiz.yaml",
        {
            "questions": [
                {
                    "id": "cap-01-q01",
                    "type": "mcq",
                    "tags": ["rag"],
                    "answer": 0,
                    "en": {"prompt": "Q", "options": ["A", "B"]},
                    "vi": {"prompt": "Q", "options": ["A", "B"]},
                }
            ],
            "flashcards": [
                {
                    "id": "cap-01-fc01",
                    "en": {"front": "F", "back": "B"},
                    "vi": {"front": "F", "back": "B"},
                }
            ],
        },
    )

    assert build_content.main(curriculum=cur, out=out, web=None) == 0

    catalog = json.loads((out / "catalog.json").read_text(encoding="utf-8"))
    assert len(catalog["phases"]) == 1
    assert catalog["phases"][0]["lessons"][0]["ready"] is True

    cap1, cap2 = catalog["capstones"]
    assert cap1["id"] == "cap-01-rag-chatbot"
    assert cap1["ready"] is True
    assert cap1["order"] == 1
    assert cap1["kind"] == "project"
    assert cap1["runner"] == "local"
    assert cap1["prerequisites"] == ["p0-01-intro"]
    assert cap1["summary"] == {"en": "Build RAG", "vi": "Xay RAG"}
    assert cap1["duration"] == 60
    assert cap1["tags"] == ["rag"]
    assert cap1["exerciseIds"] == ["cap-01-ex01"]
    assert cap1["questionCount"] == 1

    cap1_file = out / "lessons" / "cap-01-rag-chatbot.json"
    assert cap1_file.exists()
    cap1_data = json.loads(cap1_file.read_text(encoding="utf-8"))
    assert cap1_data["meta"]["runner"] == "local"
    assert cap1_data["exercises"][0]["runner"] == "local"

    review = json.loads((out / "review.json").read_text(encoding="utf-8"))
    assert [q["lessonId"] for q in review["questions"]] == ["cap-01-rag-chatbot"]
    assert [c["lessonId"] for c in review["flashcards"]] == ["cap-01-rag-chatbot"]

    assert cap2["id"] == "cap-02-tool-agent"
    assert cap2["ready"] is False
    assert cap2["order"] == 2
    assert cap2["title"] == {"en": "Agent Cap", "vi": "Agent Cap"}
    assert cap2["prerequisites"] == ["p0-01-intro"]
    assert not (out / "lessons" / "cap-02-tool-agent.json").exists()
