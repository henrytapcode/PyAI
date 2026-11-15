# Measure test accuracy before and after fine-tuning BERT-Tiny for 10 epochs on CPU.
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers import logging as hf_logging

hf_logging.set_verbosity_error()  # hide the expected LOAD REPORT on stderr
hf_logging.disable_progress_bar()
REPO = "google/bert_uncased_L-2_H-128_A-2"
REV = "30b0a37ccaaa32f332884b96992754e246e48c5f"


def make_tickets():
    bug_s = ["Login page", "Export tool", "Search API", "Mobile app", "File upload", "Dashboard"]
    bug_v = ["crashes with 500", "freezes on click", "returns blank data",
             "throws a timeout", "loops forever", "drops the session"]
    bill_s = ["Credit card", "Monthly invoice", "Annual plan",
              "Team seat", "Pro renewal", "Tax receipt"]
    bill_v = ["was charged twice", "shows wrong total", "failed to refund",
              "billed after cancel", "pending too long", "expired too early"]
    extra_bug = ["App crashed during checkout and charged me", "Screen went blank after payment click",
                 "Timeout right when submitting receipt", "UI froze while updating billing info"]
    extra_bill = ["Duplicate deduction on corporate card", "Overcharged for inactive workspace seats",
                  "Coupon ignored on final statement", "Paid for upgrade but fee doubled"]
    bugs = [f"{s} {v}" for s in bug_s for v in bug_v] + extra_bug
    bills = [f"{s} {v}" for s in bill_s for v in bill_v] + extra_bill
    return bugs + bills, [0] * len(bugs) + [1] * len(bills)


def accuracy(model, tokenizer, xs, ys):
    model.eval()
    batch = tokenizer(xs, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        preds = model(**batch).logits.argmax(dim=1)
    y_t = torch.tensor(ys, dtype=torch.int64)
    return round((preds == y_t).to(torch.float32).mean().item(), 3)


texts, labels = make_tickets()
g = torch.Generator().manual_seed(27)
idx = torch.randperm(len(texts), generator=g).tolist()
train_x, train_y = [texts[i] for i in idx[:48]], [labels[i] for i in idx[:48]]
test_x, test_y = [texts[i] for i in idx[64:]], [labels[i] for i in idx[64:]]

tokenizer = AutoTokenizer.from_pretrained(REPO, revision=REV, local_files_only=True)
torch.manual_seed(0)
model = AutoModelForSequenceClassification.from_pretrained(
    REPO,
    revision=REV,
    local_files_only=True,
    num_labels=2,
    id2label={0: "bug", 1: "billing"},
    label2id={"bug": 0, "billing": 1},
)

before = accuracy(model, tokenizer, test_x, test_y)
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-4)
train_batch = tokenizer(train_x, padding=True, truncation=True, return_tensors="pt")
train_y_t = torch.tensor(train_y, dtype=torch.int64)

for _ in range(10):
    model.train()
    optimizer.zero_grad()
    out = model(**train_batch, labels=train_y_t)
    out.loss.backward()
    optimizer.step()

after = accuracy(model, tokenizer, test_x, test_y)
print("test accuracy before:", before)
print("test accuracy after: ", after)
print("gain:", round(after - before, 3))
