# Triage six chatbot user replies using an offline sentiment pipeline.
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

REPO = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
REV = "714eb0fa89d2f80546fda750413ed43d93601a13"

tokenizer = AutoTokenizer.from_pretrained(REPO, revision=REV, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(
    REPO, revision=REV, local_files_only=True
)
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

feedback = [
    "Clear steps and solved my setup issue right away.",
    "The reply ignored my question and gave a broken URL.",
    "Helpful example code, worked on the first try.",
    "Too slow and kept looping on the same error.",
    "Nice summary, very easy to follow.",
    "It made up a flag that does not exist in this CLI.",
]

results = classifier(feedback)
neg_count = 0
for text, res in zip(feedback, results, strict=True):
    label = res["label"]
    score = round(res["score"], 3)
    if label == "NEGATIVE":
        neg_count += 1
    print(f"{label}  {score}  {text}")

print(f"negative count: {neg_count}/{len(feedback)}")
