import torch
from transformers import AutoTokenizer
from transformers import logging as hf_logging

hf_logging.set_verbosity_error()  # keep stderr clean when loading cached tokenizer files
REPO = "google/bert_uncased_L-2_H-128_A-2"
REV = "30b0a37ccaaa32f332884b96992754e246e48c5f"

tokenizer = AutoTokenizer.from_pretrained(REPO, revision=REV, local_files_only=True)


def split_data(
    texts: list[str],
    labels: list[int],
    val_frac: float,
    test_frac: float,
    seed: int,
) -> tuple[list[str], list[int], list[str], list[int], list[str], list[int]]:
    """Split texts and labels into train, val, and test using a seeded torch.randperm.

    Example: split_data(["a", "b", "c", "d", "e"], [0, 1, 0, 1, 0], 0.2, 0.2, 0)
    -> 3 train items, 1 val item, 1 test item.
    """
    n = len(texts)
    n_val = int(n * val_frac)
    n_test = int(n * test_frac)
    n_train = n - n_val - n_test

    gen = torch.Generator().manual_seed(seed)
    idx = torch.randperm(n, generator=gen).tolist()
    tr, va, te = idx[:n_train], idx[n_train : n_train + n_val], idx[n_train + n_val :]
    return (
        [texts[i] for i in tr],
        [labels[i] for i in tr],
        [texts[i] for i in va],
        [labels[i] for i in va],
        [texts[i] for i in te],
        [labels[i] for i in te],
    )


def encode(texts: list[str], max_length: int) -> dict[str, torch.Tensor]:
    """Tokenize texts with padding, truncation to max_length, and return_tensors='pt'.

    Example: encode(["App crashes"], max_length=16) -> {"input_ids": ..., "attention_mask": ...}
    """
    batch = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )
    return {
        "input_ids": batch["input_ids"],
        "attention_mask": batch["attention_mask"],
    }


def class_counts(labels: list[int]) -> dict[int, int]:
    """Return {label: count} for the given list of integer labels.

    Example: class_counts([0, 1, 0]) -> {0: 2, 1: 1}
    """
    counts: dict[int, int] = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1
    return counts
