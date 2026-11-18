# Score two golden dialogs and compare results against a baseline run.
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

dialogs = [
    {
        "id": "d1",
        "turns": [
            {"question": "How long are store pickup orders held?", "expected_source": "pickup.md", "expected_facts": ["7 days"]},
            {"question": "And photo ID?", "expected_source": "pickup.md", "expected_facts": ["photo ID"]},
        ],
    },
    {
        "id": "d2",
        "turns": [
            {"question": "When do support agents work on weekdays?", "expected_source": "support.md", "expected_facts": ["Monday to Friday"]},
            {"question": "Do you offer cryptocurrency billing?", "expected_source": None, "expected_facts": []},
        ],
    },
]

client = FakeLLM(embed_dim=256)
chunks = [
    {"id": f"{d['source']}#{i}", "source": d["source"], "text": s.strip()}
    for d in docs
    for i, s in enumerate(re.split(r"(?<=[.!?])\s+", d["text"].strip()))
    if s.strip()
]
vecs = np.array(client.embed([c["text"] for c in chunks]), dtype=float)


def eval_dialogs(rewrite: bool, min_score: float) -> dict[str, bool]:
    results: dict[str, bool] = {}
    for dlg in dialogs:
        prev_user = ""
        for idx, turn in enumerate(dlg["turns"], 1):
            q = turn["question"]
            low = q.lower().strip()
            if rewrite and prev_user and (len(q.split()) <= 4 or low.startswith(("what about ", "and ", "how about "))):
                query = f"{prev_user} {q}"
            else:
                query = q
            prev_user = q
            q_vec = np.array(client.embed([query])[0], dtype=float)
            scores = vecs @ q_vec
            order = np.argsort(-scores, kind="stable")[:2]
            hits = [chunks[int(i)] for i in order if float(scores[int(i)]) >= min_score]
            if not hits:
                ans = "I don't know based on the provided context."
            else:
                ctx = "\n".join(f"[{n}] {h['text']}" for n, h in enumerate(hits, 1))
                ans = client.chat([
                    {"role": "system", "content": "Context:\n" + ctx},
                    {"role": "user", "content": query},
                ]).content or ""
            exp = turn["expected_source"]
            if exp is None:
                ok = "i don't know" in ans.lower()
            else:
                ok = (
                    exp in [h["source"] for h in hits]
                    and all(f.lower() in ans.lower() for f in turn["expected_facts"])
                )
            results[f"{dlg['id']}#t{idx}"] = ok
    return results


baseline = eval_dialogs(rewrite=False, min_score=0.2)
current = eval_dialogs(rewrite=True, min_score=0.35)

fixed = [k for k in current if current[k] and not baseline[k]]
broken = [k for k in current if not current[k] and baseline[k]]

print(f"{'case':<8} {'baseline':<10} {'current':<10}")
for key in current:
    b_str = "PASS" if baseline[key] else "FAIL"
    c_str = "PASS" if current[key] else "FAIL"
    print(f"{key:<8} {b_str:<10} {c_str:<10}")
print("fixed :", fixed)
print("broken:", broken)
