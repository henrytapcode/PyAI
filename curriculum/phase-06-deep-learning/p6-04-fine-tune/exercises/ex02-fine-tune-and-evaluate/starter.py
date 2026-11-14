import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import logging as hf_logging

hf_logging.set_verbosity_error()  # hide the expected LOAD REPORT on stderr
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
    # TODO: call model.eval(), tokenize texts, run no_grad() forward pass, return rounded float
    return None


def fine_tune(model, texts: list[str], labels: list[int], lr: float, epochs: int) -> list[float]:
    """Run full-batch AdamW fine-tuning and return per-epoch losses rounded to 4 decimals.

    Example: fine_tune(model, texts, labels, lr=5e-4, epochs=3) -> [0.6913, 0.6512, 0.6104]
    """
    # TODO: handle epochs <= 0, train full-batch with AdamW and model(**batch, labels=y)
    return None


def predict(model, texts: list[str]) -> list[str]:
    """Predict string class labels ('bug' or 'billing') using model.config.id2label.

    Example: predict(model, ["Charged twice"]) -> ["billing"]
    """
    # TODO: call model.eval(), run no_grad() forward pass, map argmax IDs via id2label
    return None
