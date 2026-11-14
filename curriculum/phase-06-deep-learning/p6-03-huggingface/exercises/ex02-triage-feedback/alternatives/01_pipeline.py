from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

REPO = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
REV = "714eb0fa89d2f80546fda750413ed43d93601a13"

tokenizer = AutoTokenizer.from_pretrained(REPO, revision=REV, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(
    REPO, revision=REV, local_files_only=True
)


def classify(texts: list[str]) -> list[tuple[str, float]]:
    """Return (label, rounded_score) for each text using transformers.pipeline()."""
    if not texts:
        return []
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    return [(item["label"], round(float(item["score"]), 3)) for item in classifier(texts)]


def negatives(texts: list[str], threshold: float) -> list[str]:
    """Return texts predicted as NEGATIVE with score >= threshold in original order."""
    if not texts:
        return []
    return [
        text
        for text, (label, score) in zip(texts, classify(texts), strict=True)
        if label == "NEGATIVE" and score >= threshold
    ]
