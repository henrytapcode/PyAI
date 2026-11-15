# Compare configs on dev_set, pick one, and score test_set once.
import re
import numpy as np
from pyai_llm import FakeLLM

docs = [
    {"source": "refunds.md", "text": "Refunds are issued within 30 days of purchase. Keep your original receipt for any return. Opened software is not eligible for a refund."},
    {"source": "shipping.md", "text": "Standard shipping takes 5 business days across the country. Express delivery arrives next day for 12 dollars. Free shipping applies on orders over 50 dollars."},
    {"source": "warranty.md", "text": "Hardware warranty covers factory defects for 12 months. Water damage and dropped screens are not covered. Battery wear after 6 months is excluded."},
    {"source": "payment.md", "text": "Accepted payment methods are Visa, Mastercard, and cash on delivery. Gift cards cannot be redeemed for cash. Invoices are emailed right after checkout."},
    {"source": "accounts.md", "text": "Password resets are sent by email within 5 minutes. Two-factor login can be turned on in security settings. Inactive accounts remain open for 24 months."},
    {"source": "support.md", "text": "Support agents work Monday to Friday from 9 AM to 6 PM. Weekend messages receive replies on Monday morning. Urgent outage tickets get a 2 hour target."},
    {"source": "pickup.md", "text": "Store pickup is ready 2 hours after order confirmation. Unclaimed orders are held at the counter for 7 days. Bring a photo ID at pickup."},
    {"source": "discounts.md", "text": "Student discounts give 15 percent off eligible laptops. Promo codes cannot be combined on one order. Loyalty points expire after 12 months."},
]

dev_set = [
    {"id": "d1", "question": "How many days do refunds take after purchase?", "expected_source": "refunds.md", "expected_facts": ["30 days"]},
    {"id": "d2", "question": "How much does express delivery cost?", "expected_source": "shipping.md", "expected_facts": ["12 dollars"]},
    {"id": "d3", "question": "How long is hardware warranty for factory defects?", "expected_source": "warranty.md", "expected_facts": ["12 months"]},
    {"id": "d4", "question": "What payment methods are accepted at checkout?", "expected_source": "payment.md", "expected_facts": ["Visa", "Mastercard"]},
    {"id": "d5", "question": "How quickly do password resets arrive by email?", "expected_source": "accounts.md", "expected_facts": ["5 minutes"]},
    {"id": "d6", "question": "Can I get money back within a month?", "expected_source": "refunds.md", "expected_facts": ["30 days"]},
    {"id": "d7", "question": "Do you offer cryptocurrency billing?", "expected_source": None, "expected_facts": []},
    {"id": "d8", "question": "Can I pay with crypto for online orders?", "expected_source": None, "expected_facts": []},
]

test_set = [
    {"id": "t1", "question": "When do support agents work on weekdays?", "expected_source": "support.md", "expected_facts": ["Monday to Friday", "9 AM to 6 PM"]},
    {"id": "t2", "question": "How many days are unclaimed pickup orders held?", "expected_source": "pickup.md", "expected_facts": ["7 days"]},
    {"id": "t3", "question": "How much off do students get on notebooks?", "expected_source": "discounts.md", "expected_facts": ["15 percent"]},
    {"id": "t4", "question": "Is international customs insurance included?", "expected_source": None, "expected_facts": []},
]


def chunk_text(text: str, mode: str, size: int = 8, overlap: int = 2) -> list[str]:
    if mode == "sentence":
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    words = text.split()
    step = size - overlap
    out: list[str] = []
    i = 0
    while i < len(words):
        out.append(" ".join(words[i : i + size]))
        if i + size >= len(words):
            break
        i += step
    return out


def run_split(split: list[dict], mode: str, k: int, min_score: float) -> dict:
    client = FakeLLM(embed_dim=256)
    chunks = [
        {"id": f"{d['source']}#{i}", "source": d["source"], "text": piece}
        for d in docs
        for i, piece in enumerate(chunk_text(d["text"], mode))
    ]
    vecs = np.array(client.embed([c["text"] for c in chunks]), dtype=float)
    hits = n_ans = facts_ok = idk_ok = n_idk = 0
    failures: list[tuple[str, str]] = []
    for row in split:
        q_vec = np.array(client.embed([row["question"]])[0], dtype=float)
        scores = vecs @ q_vec
        order = np.argsort(-scores, kind="stable")[:k]
        top_hits = [chunks[int(i)] for i in order if float(scores[int(i)]) >= min_score]
        ctx = "\n".join(f"[{n}] {h['text']}" for n, h in enumerate(top_hits, 1))
        ans = (
            client.chat([{"role": "system", "content": "Context:\n" + ctx}, {"role": "user", "content": row["question"]}]).content
            or ""
            if top_hits
            else "I don't know based on the provided context."
        )
        exp = row["expected_source"]
        if exp is None:
            n_idk += 1
            if "i don't know" in ans.lower():
                idk_ok += 1
            else:
                failures.append((row["id"], "no_refusal"))
        else:
            n_ans += 1
            h_ok = exp in [h["source"] for h in top_hits]
            f_ok = all(f.lower() in ans.lower() for f in row["expected_facts"])
            hits += int(h_ok)
            facts_ok += int(f_ok)
            if not h_ok:
                failures.append((row["id"], "retrieval_miss"))
            elif not f_ok:
                failures.append((row["id"], "answer_miss"))
    return {"hits": hits, "n_ans": n_ans, "facts": facts_ok, "idk": idk_ok, "n_idk": n_idk, "failures": failures}


def fmt(num: int, den: int) -> str:
    return f"{num}/{den} ({round(num / den * 100)}%)"


candidates = [
    ("words(8,2) m=0.2", "words", 2, 0.2),
    ("sent k=2 m=0.2", "sentence", 2, 0.2),
    ("sent k=2 m=0.35", "sentence", 2, 0.35),
]
dev_results = [(label, mode, k, ms, run_split(dev_set, mode, k, ms)) for label, mode, k, ms in candidates]
for label, _, _, _, s in dev_results:
    print(f"dev {label:<16}: hit={fmt(s['hits'], s['n_ans'])} facts={fmt(s['facts'], s['n_ans'])} idk={fmt(s['idk'], s['n_idk'])}")

best_label, best_mode, best_k, best_ms, best_dev = max(
    dev_results,
    key=lambda item: (item[4]["facts"], item[4]["idk"], item[4]["hits"]),
)
test_res = run_split(test_set, best_mode, best_k, best_ms)
print("chosen:", best_label)
print(f"test {best_label:<15}: hit={fmt(test_res['hits'], test_res['n_ans'])} facts={fmt(test_res['facts'], test_res['n_ans'])} idk={fmt(test_res['idk'], test_res['n_idk'])}")
for qid, reason in best_dev["failures"]:
    print(f"dev  FAIL {qid}: {reason}")
for qid, reason in test_res["failures"]:
    print(f"test FAIL {qid}: {reason}")
