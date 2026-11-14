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
    if not texts:
        return []
    batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    model.eval()
    with torch.no_grad():
        logits = model(**batch).logits
    probs = torch.softmax(logits, dim=1)
    pred_ids = logits.argmax(dim=1)
    return [
        (model.config.id2label[idx], round(float(prob_row[idx]), 3))
        for prob_row, idx in zip(probs.tolist(), pred_ids.tolist(), strict=True)
    ]


def negatives(texts: list[str], threshold: float) -> list[str]:
    """Return texts predicted as NEGATIVE with score >= threshold in original order.

    Example: negatives(["Great!", "Terrible."], 0.9) -> ["Terrible."]
    """
    if not texts:
        return []
    return [
        text
        for text, (label, score) in zip(texts, classify(texts), strict=True)
        if label == "NEGATIVE" and score >= threshold
    ]
