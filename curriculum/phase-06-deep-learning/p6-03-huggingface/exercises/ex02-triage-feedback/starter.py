import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

REPO = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
REV = "714eb0fa89d2f80546fda750413ed43d93601a13"

tokenizer = AutoTokenizer.from_pretrained(REPO, revision=REV, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(
    REPO, revision=REV, local_files_only=True
)


def classify(texts: list[str]) -> list[tuple[str, float]]:
    """Return (label, rounded_score) for each text without using pipeline().

    Example: classify(["Great!", "Terrible."]) -> [("POSITIVE", 1.0), ("NEGATIVE", 1.0)]
    """
    # TODO: handle empty texts, tokenize with padding/truncation, run model.eval() + no_grad()
    # TODO: compute softmax, argmax, map via model.config.id2label, and return rounded scores
    return None


def negatives(texts: list[str], threshold: float) -> list[str]:
    """Return texts predicted as NEGATIVE with score >= threshold in original order.

    Example: negatives(["Great!", "Terrible."], 0.9) -> ["Terrible."]
    """
    # TODO: call classify(texts) and keep NEGATIVE items whose score >= threshold
    return None
