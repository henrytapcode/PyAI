# Fine-tune BERT-Tiny, save to a temporary folder, reload, and predict 4 new tickets.
import tempfile

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
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


texts, labels = make_tickets()
g = torch.Generator().manual_seed(27)
idx = torch.randperm(len(texts), generator=g).tolist()
train_x, train_y = [texts[i] for i in idx[:48]], [labels[i] for i in idx[:48]]

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

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-4)
train_batch = tokenizer(train_x, padding=True, truncation=True, return_tensors="pt")
train_y_t = torch.tensor(train_y, dtype=torch.int64)

for _ in range(10):
    model.train()
    optimizer.zero_grad()
    out = model(**train_batch, labels=train_y_t)
    out.loss.backward()
    optimizer.step()

new_tickets = [
    "Settings page throws a 500 error",
    "Invoice shows duplicate card charge",
    "Dashboard freezes when loading report",
    "Need a refund for double billing",
]

with tempfile.TemporaryDirectory() as tmp:
    model.save_pretrained(tmp)
    tokenizer.save_pretrained(tmp)
    reloaded_model = AutoModelForSequenceClassification.from_pretrained(tmp)
    reloaded_tokenizer = AutoTokenizer.from_pretrained(tmp)
    clf = pipeline("text-classification", model=reloaded_model, tokenizer=reloaded_tokenizer)
    for text, res in zip(new_tickets, clf(new_tickets), strict=True):
        print(f"{res['label']}  {text}")
