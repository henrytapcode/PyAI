"""Pinned Hugging Face models required for local-runner curriculum lessons.

Lessons load cached models offline using the pinned ``repo_id`` and ``revision``::

    from transformers import AutoModelForSequenceClassification

    model = AutoModelForSequenceClassification.from_pretrained(
        REPO, revision=REV, local_files_only=True
    )
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

IGNORE_PATTERNS: list[str] = [
    "tf_model.h5",
    "flax_model.msgpack",
    "*.onnx",
    "rust_model.ot",
    "coreml/*",
    "onnx/*",
]

MODELS: list[dict[str, Any]] = [
    {
        "key": "sentiment",
        "repo_id": "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
        "revision": "714eb0fa89d2f80546fda750413ed43d93601a13",
        "purpose": "p6-03: pipeline('sentiment-analysis') inference",
        "allow_patterns": ["*.json", "*.txt", "*.safetensors"],
    },
    {
        "key": "tiny-bert",
        "repo_id": "google/bert_uncased_L-2_H-128_A-2",
        "revision": "30b0a37ccaaa32f332884b96992754e246e48c5f",
        "purpose": "p6-04: fine-tune a tiny classifier on CPU",
        "allow_patterns": ["*.json", "*.txt", "*.safetensors"],
    },
]

_MODELS_BY_KEY: dict[str, dict[str, Any]] = {m["key"]: m for m in MODELS}


def get_model(key: str) -> dict[str, Any]:
    """Return the model metadata dictionary for ``key`` or raise ``KeyError``."""
    return _MODELS_BY_KEY[key]


def resolve_cache_dir(cache_dir: str | Path | None = None) -> str | None:
    """Resolve the HF Hub cache directory at call time so env overrides take effect."""
    if cache_dir is not None:
        return str(cache_dir)
    env_cache = os.environ.get("HF_HUB_CACHE") or os.environ.get("HUGGINGFACE_HUB_CACHE")
    if env_cache:
        return env_cache
    hf_home = os.environ.get("HF_HOME")
    if hf_home:
        return str(Path(hf_home) / "hub")
    return None


def model_path(key: str, cache_dir: str | Path | None = None) -> str | None:
    """Return the local snapshot directory for ``key``, or ``None`` if not cached."""
    model = get_model(key)
    from huggingface_hub import snapshot_download
    from huggingface_hub.errors import LocalEntryNotFoundError

    try:
        return str(
            snapshot_download(
                model["repo_id"],
                revision=model["revision"],
                cache_dir=resolve_cache_dir(cache_dir),
                local_files_only=True,
                allow_patterns=model["allow_patterns"],
                ignore_patterns=IGNORE_PATTERNS,
            )
        )
    except (LocalEntryNotFoundError, OSError):
        return None


def missing_models(cache_dir: str | Path | None = None) -> list[str]:
    """Return keys of pinned models not currently present in the local cache."""
    return [m["key"] for m in MODELS if model_path(m["key"], cache_dir=cache_dir) is None]
