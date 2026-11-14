from collections import Counter

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
    n = len(texts)
    n_val = int(n * val_frac)
    n_test = int(n * test_frac)
    n_train = n - n_val - n_test

    gen = torch.Generator().manual_seed(seed)
    perm = torch.randperm(n, generator=gen).tolist()

    train_x, train_y = [], []
    val_x, val_y = [], []
    test_x, test_y = [], []
    val_end = n_train + n_val

    for pos, idx in enumerate(perm):
        if pos < n_train:
            train_x.append(texts[idx])
            train_y.append(labels[idx])
        elif pos < val_end:
            val_x.append(texts[idx])
            val_y.append(labels[idx])
        else:
            test_x.append(texts[idx])
            test_y.append(labels[idx])

    return train_x, train_y, val_x, val_y, test_x, test_y


def encode(texts: list[str], max_length: int) -> dict[str, torch.Tensor]:
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
    return dict(Counter(labels))
