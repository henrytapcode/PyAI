"""Tests for pinned Hugging Face model registry, fetcher, and validate hook."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tools import validate
from tools.localrunner import fetch_models
from tools.localrunner.models import MODELS, get_model, missing_models, model_path

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPO_ROOT = Path(__file__).resolve().parents[2]


def test_models_have_unique_keys_and_40_hex_revisions():
    keys = [m["key"] for m in MODELS]
    assert len(keys) == len(set(keys))
    assert len(MODELS) >= 2
    for m in MODELS:
        assert SHA_RE.fullmatch(m["revision"]), f"{m['key']} revision is not 40-char hex"
        assert m["repo_id"]
        assert m["allow_patterns"]


def test_missing_models_with_empty_cache(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv("HF_HUB_CACHE", str(tmp_path))
    expected = [m["key"] for m in MODELS]
    assert missing_models() == expected
    assert missing_models(cache_dir=tmp_path) == expected
    for key in expected:
        assert model_path(key) is None


def test_fetch_models_check_empty_cache_exits_1(tmp_path: Path):
    env = dict(os.environ, HF_HUB_CACHE=str(tmp_path), PYTHONUTF8="1")
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "localrunner" / "fetch_models.py"), "--check"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        cwd=REPO_ROOT,
    )
    assert proc.returncode == 1
    combined = proc.stdout + proc.stderr
    for m in MODELS:
        assert m["key"] in combined


def test_fetch_models_check_inprocess_empty_cache(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    monkeypatch.setenv("HF_HUB_CACHE", str(tmp_path))
    rc = fetch_models.main(["--check"])
    captured = capsys.readouterr()
    assert rc == 1
    for m in MODELS:
        assert m["key"] in captured.out


def test_lessons_needing_models(tmp_path: Path):
    sentiment = get_model("sentiment")
    tiny = get_model("tiny-bert")

    les_py = tmp_path / "p6-03-huggingface"
    (les_py / "examples").mkdir(parents=True)
    (les_py / "examples" / "demo.py").write_text(
        f'REPO = "{sentiment["repo_id"]}"\n', encoding="utf-8"
    )

    les_md = tmp_path / "p6-04-fine-tune"
    les_md.mkdir()
    (les_md / "lesson.en.md").write_text(
        f"We fine-tune `{tiny['repo_id']}` on CPU.\n", encoding="utf-8"
    )

    les_none = tmp_path / "p6-01-tensors"
    les_none.mkdir()
    (les_none / "lesson.en.md").write_text("Pure PyTorch tensors.\n", encoding="utf-8")
    # Non-.py/.md files should not trigger a model dependency.
    (les_none / "notes.yaml").write_text(f"repo: {sentiment['repo_id']}\n", encoding="utf-8")

    result = validate.lessons_needing_models([les_py, les_md, les_none], MODELS)
    assert result == {
        les_py: ["sentiment"],
        les_md: ["tiny-bert"],
    }


_OFFLINE_TEST_SCRIPT = """
import json
import os
import warnings

assert os.environ.get("HF_HUB_OFFLINE") == "1"

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
)
from tools.localrunner.models import get_model

sentiment = get_model("sentiment")
s_tok = AutoTokenizer.from_pretrained(
    sentiment["repo_id"], revision=sentiment["revision"], local_files_only=True
)
s_mdl = AutoModelForSequenceClassification.from_pretrained(
    sentiment["repo_id"], revision=sentiment["revision"], local_files_only=True
)
clf = pipeline("sentiment-analysis", model=s_mdl, tokenizer=s_tok)
texts = ["I love this course", "This is terrible"]
first = clf(texts)
second = clf(texts)

tiny = get_model("tiny-bert")
t_tok = AutoTokenizer.from_pretrained(
    tiny["repo_id"], revision=tiny["revision"], local_files_only=True
)
tiny_lowercase_ok = t_tok("Hello")["input_ids"] == t_tok("hello")["input_ids"]
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    t_mdl = AutoModelForSequenceClassification.from_pretrained(
        tiny["repo_id"], revision=tiny["revision"], num_labels=2, local_files_only=True
    )
batch = t_tok(texts, padding=True, return_tensors="pt")
logits = t_mdl(**batch).logits

print(json.dumps({
    "first_labels": [r["label"] for r in first],
    "first_scores": [round(r["score"], 4) for r in first],
    "second_scores": [round(r["score"], 4) for r in second],
    "tiny_lowercase_ok": tiny_lowercase_ok,
    "logits_shape": list(logits.shape),
}))
"""


@pytest.mark.skipif(bool(missing_models()), reason="Pinned HF models not cached locally")
def test_cached_models_offline_inference():
    # Run in a subprocess so importing torch/transformers does not pollute sys.modules
    # for test_server.py::test_health, and so HF_HUB_OFFLINE=1 applies from import time.
    env = dict(os.environ)
    env["HF_HUB_OFFLINE"] = "1"
    env["TRANSFORMERS_OFFLINE"] = "1"
    env["PYTHONUTF8"] = "1"
    existing_pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        f"{REPO_ROOT}{os.pathsep}{existing_pp}" if existing_pp else str(REPO_ROOT)
    )
    proc = subprocess.run(
        [sys.executable, "-c", _OFFLINE_TEST_SCRIPT],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        cwd=REPO_ROOT,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    data = json.loads(proc.stdout.strip().splitlines()[-1])
    assert data["first_labels"] == ["POSITIVE", "NEGATIVE"]
    assert data["first_scores"] == data["second_scores"]
    assert data["tiny_lowercase_ok"] is True
    assert data["logits_shape"] == [2, 2]
