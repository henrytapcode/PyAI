import torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import logging as hf_logging

hf_logging.set_verbosity_error()  # hide the expected LOAD REPORT on stderr
REPO = "google/bert_uncased_L-2_H-128_A-2"
REV = "30b0a37ccaaa32f332884b96992754e246e48c5f"

tokenizer = AutoTokenizer.from_pretrained(REPO, revision=REV, local_files_only=True)


def load_model():
    torch.manual_seed(0)
    return AutoModelForSequenceClassification.from_pretrained(
        REPO,
        revision=REV,
        local_files_only=True,
        num_labels=2,
        id2label={0: "bug", 1: "billing"},
        label2id={"bug": 0, "billing": 1},
    )


def accuracy(model, texts: list[str], labels: list[int]) -> float:
    model.eval()
    batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        preds = model(**batch).logits.argmax(dim=1)
    y = torch.tensor(labels, dtype=torch.int64)
    return round(float((preds == y).float().mean().item()), 3)


def fine_tune(model, texts: list[str], labels: list[int], lr: float, epochs: int) -> list[float]:
    if epochs <= 0:
        return []
    batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    y = torch.tensor(labels, dtype=torch.int64)
    dataset = TensorDataset(batch["input_ids"], batch["attention_mask"], y)
    gen = torch.Generator().manual_seed(0)
    loader = DataLoader(dataset, batch_size=8, shuffle=True, num_workers=0, generator=gen)

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    losses: list[float] = []
    for _ in range(epochs):
        model.train()
        total_loss = 0.0
        for input_ids, attention_mask, yb in loader:
            optimizer.zero_grad()
            out = model(input_ids=input_ids, attention_mask=attention_mask, labels=yb)
            out.loss.backward()
            optimizer.step()
            total_loss += float(out.loss.item())
        losses.append(round(total_loss / len(loader), 4))
    return losses


def predict(model, texts: list[str]) -> list[str]:
    model.eval()
    batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        pred_ids = model(**batch).logits.argmax(dim=1)
    return [model.config.id2label[idx] for idx in pred_ids.tolist()]
