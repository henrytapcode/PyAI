# Generate 80 support tickets, split train/val/test, and inspect counts and max tokens.
import torch
from transformers import AutoTokenizer
from transformers import logging as hf_logging

hf_logging.set_verbosity_error()  # keep stderr clean when loading cached files
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

splits = {
    "train": ([texts[i] for i in idx[:48]], [labels[i] for i in idx[:48]]),
    "val": ([texts[i] for i in idx[48:64]], [labels[i] for i in idx[48:64]]),
    "test": ([texts[i] for i in idx[64:]], [labels[i] for i in idx[64:]]),
}
for name, (xs, ys) in splits.items():
    print(f"{name:5s} total={len(xs)} bug={ys.count(0)} billing={ys.count(1)}")

tokenizer = AutoTokenizer.from_pretrained(REPO, revision=REV, local_files_only=True)
lengths = [len(tokenizer(t)["input_ids"]) for t in texts]
print("max token length:", max(lengths))
