"""Download and verify pinned Hugging Face models for offline local-runner lessons."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.localrunner.models import (  # noqa: E402
    IGNORE_PATTERNS,
    MODELS,
    model_path,
    resolve_cache_dir,
)


def _snapshot_size_mb(snapshot_dir: str | Path) -> float:
    total = sum(p.stat().st_size for p in Path(snapshot_dir).rglob("*") if p.is_file())
    return total / (1024 * 1024)


def _check_models() -> int:
    missing = []
    for model in MODELS:
        key = model["key"]
        path = model_path(key)
        if path is None:
            missing.append(key)
            print(f"{key}: missing ({model['repo_id']}@{model['revision'][:12]})")
        else:
            size_mb = _snapshot_size_mb(path)
            print(f"{key}: cached ({size_mb:.2f} MB) {path}")
    if missing:
        print(
            f"Missing {len(missing)} model(s): {', '.join(missing)}. "
            "Run: uv run python tools/localrunner/fetch_models.py",
            file=sys.stderr,
        )
        return 1
    return 0


_OFFLINE_CHECK_CODE = """
import os
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    pipeline,
)
from tools.localrunner.models import MODELS

assert os.environ.get("HF_HUB_OFFLINE") == "1"

for m in MODELS:
    key = m["key"]
    repo = m["repo_id"]
    rev = m["revision"]
    tok = AutoTokenizer.from_pretrained(repo, revision=rev, local_files_only=True)
    if key == "tiny-bert":
        if tok("Hello")["input_ids"] != tok("hello")["input_ids"]:
            raise RuntimeError("Expected uncased tokenization for tiny-bert")
        mdl = AutoModelForSequenceClassification.from_pretrained(
            repo, revision=rev, num_labels=2, local_files_only=True
        )
        inputs = tok(["Hello world", "Second sentence"], padding=True, return_tensors="pt")
        out = mdl(**inputs)
        if tuple(out.logits.shape) != (2, 2):
            raise RuntimeError(f"Unexpected tiny-bert logits shape: {tuple(out.logits.shape)}")
        print(f"offline-check {key}: logits {tuple(out.logits.shape)}")
    else:
        mdl = AutoModelForSequenceClassification.from_pretrained(
            repo, revision=rev, local_files_only=True
        )
        if key == "sentiment":
            clf = pipeline("sentiment-analysis", model=mdl, tokenizer=tok)
            res = clf("This course makes Python clear and practical.")
            if not res or "label" not in res[0]:
                raise RuntimeError(f"Unexpected sentiment pipeline output: {res!r}")
            print(f"offline-check {key}: {res[0]['label']} ({res[0]['score']:.4f})")
"""


def _verify_offline() -> int:
    env = dict(os.environ)
    env["HF_HUB_OFFLINE"] = "1"
    env["TRANSFORMERS_OFFLINE"] = "1"
    env["PYTHONUTF8"] = "1"
    existing_pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        f"{_REPO_ROOT}{os.pathsep}{existing_pp}" if existing_pp else str(_REPO_ROOT)
    )
    proc = subprocess.run(
        [sys.executable, "-c", _OFFLINE_CHECK_CODE],
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.stdout.strip():
        print(proc.stdout.strip())
    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or f"exit code {proc.returncode}"
        print(f"Offline self-check failed:\n{detail}", file=sys.stderr)
        return 1
    return 0


def _fetch_models() -> int:
    from huggingface_hub import snapshot_download

    cache_dir = resolve_cache_dir(None)
    for model in MODELS:
        key = model["key"]
        cached = model_path(key, cache_dir=cache_dir)
        if cached is not None:
            size_mb = _snapshot_size_mb(cached)
            print(f"{key}: already cached ({size_mb:.2f} MB) {cached}")
            continue
        try:
            path = snapshot_download(
                model["repo_id"],
                revision=model["revision"],
                cache_dir=cache_dir,
                allow_patterns=model["allow_patterns"],
                ignore_patterns=IGNORE_PATTERNS,
            )
        except Exception as exc:  # noqa: BLE001 - surface clear download failure to CLI
            print(f"Failed to download {key} ({model['repo_id']}): {exc}", file=sys.stderr)
            return 1
        size_mb = _snapshot_size_mb(path)
        print(f"{key}: {size_mb:.2f} MB {path}")

    return _verify_offline()


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Fetch or check cached Hugging Face models for local-runner lessons."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify models are cached offline without contacting the Hub.",
    )
    args = parser.parse_args(argv)

    if args.check:
        return _check_models()
    return _fetch_models()


if __name__ == "__main__":
    sys.exit(main())
