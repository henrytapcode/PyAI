import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import logging as hf_logging

hf_logging.set_verbosity_error()  # hide the expected LOAD REPORT on stderr
hf_logging.disable_progress_bar()
REPO = "google/bert_uncased_L-2_H-128_A-2"
REV = "30b0a37ccaaa32f332884b96992754e246e48c5f"

tokenizer = AutoTokenizer.from_pretrained(REPO, revision=REV, local_files_only=True)


def load_model():
    """Load BERT-Tiny offline with a seeded 2-class classification head."""
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
    """Evaluate classification accuracy in eval()+no_grad() mode, rounded to 3 decimals.

    Example: accuracy(model, ["Login crashes"], [0]) -> 1.0
    """
    model.eval()
    batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        preds = model(**batch).logits.argmax(dim=1)
    y = torch.tensor(labels, dtype=torch.int64)
    return round((preds == y).to(torch.float32).mean().item(), 3)


def fine_tune(model, texts: list[str], labels: list[int], lr: float, epochs: int) -> list[float]:
    """Run full-batch AdamW fine-tuning and return per-epoch losses rounded to 4 decimals.

    Example: fine_tune(model, ["Bug A", "Bill B"], [0, 1], lr=5e-4, epochs=3)
    -> a list of 3 floats, e.g. decreasing losses
    """
    if epochs <= 0:
        return []
    batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    y = torch.tensor(labels, dtype=torch.int64)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    losses: list[float] = []
    for _ in range(epochs):
        model.train()
        optimizer.zero_grad()
        out = model(**batch, labels=y)
        out.loss.backward()
        optimizer.step()
        losses.append(round(out.loss.item(), 4))
    return losses


def predict(model, texts: list[str]) -> list[str]:
    """Predict string class labels ('bug' or 'billing') using model.config.id2label.

    Example: predict(model, ["Charged twice"]) -> ["billing"]
    """
    model.eval()
    batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        pred_ids = model(**batch).logits.argmax(dim=1)
    return [model.config.id2label[idx] for idx in pred_ids.tolist()]


def pick_epoch(history: list[tuple[int, float, float]]) -> int:
    """Pick the best epoch from (epoch, val_acc, val_loss) history tuples.

    Highest val_acc wins; ties break on lowest val_loss, then earliest epoch.

    Example: pick_epoch([(1, 0.9, 0.5), (2, 0.9, 0.3)]) -> 2
    """
    best_epoch, best_acc, best_loss = history[0]
    for epoch, val_acc, val_loss in history[1:]:
        if (val_acc, -val_loss, -epoch) > (best_acc, -best_loss, -best_epoch):
            best_epoch, best_acc, best_loss = epoch, val_acc, val_loss
    return best_epoch
