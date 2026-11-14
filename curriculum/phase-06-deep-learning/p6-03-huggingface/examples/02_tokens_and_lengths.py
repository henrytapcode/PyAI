# Inspect token counts, batch padding shapes, and max_length truncation.
from transformers import AutoTokenizer

REPO = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
REV = "714eb0fa89d2f80546fda750413ed43d93601a13"

tokenizer = AutoTokenizer.from_pretrained(REPO, revision=REV, local_files_only=True)

texts = [
    "Worked!",
    "Fast and helpful answer.",
    "Chatbot reconnected after timeout.",
    "The bot repeated the same broken link three times.",
]

counts = [len(tokenizer.tokenize(text)) for text in texts]
for text, count in zip(texts, counts, strict=True):
    print(f"tokens={count:2d}  {text}")

print("longest token count:", max(counts))
batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
print("padded batch shape:", tuple(batch["input_ids"].shape))

long_text = "Users asked why the search endpoint timed out after deploying the update."
short = tokenizer(long_text, truncation=True, max_length=8)
print("truncated length:", len(short["input_ids"]))
print("truncated tokens:", tokenizer.convert_ids_to_tokens(short["input_ids"]))
