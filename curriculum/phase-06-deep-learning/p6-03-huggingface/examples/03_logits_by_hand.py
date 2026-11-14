# Compute softmax probabilities and labels by hand, then compare with pipeline().
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

REPO = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
REV = "714eb0fa89d2f80546fda750413ed43d93601a13"

tokenizer = AutoTokenizer.from_pretrained(REPO, revision=REV, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(
    REPO, revision=REV, local_files_only=True
)
model.eval()

texts = [
    "Fast and helpful answer, solved my bug!",
    "The bot kept repeating the wrong link.",
    "Thanks, that worked after I restarted.",
]

batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
with torch.no_grad():
    logits = model(**batch).logits

probs = torch.softmax(logits, dim=1)
pred_ids = logits.argmax(dim=1)

manual = []
for text, prob_row, idx in zip(texts, probs.tolist(), pred_ids.tolist(), strict=True):
    label = model.config.id2label[idx]
    score = round(prob_row[idx], 3)
    manual.append((label, score))
    print(f"{label}  {score}  {text}")

classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
from_pipe = [(res["label"], round(res["score"], 3)) for res in classifier(texts)]
print("match:", manual == from_pipe)
