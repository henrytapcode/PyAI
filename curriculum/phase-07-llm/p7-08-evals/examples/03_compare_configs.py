# Compare k=1 and k=3 on the same eval set with counts and per-question diffs.
import re
import numpy as np
from pyai_llm import FakeLLM

docs = [
    {"source": "refunds.md", "text": "Refunds are issued within 30 days of purchase. Keep your original receipt and unused item."},
    {"source": "shipping.md", "text": "Standard shipping arrives within 5 business days. Express delivery arrives the next day."},
    {"source": "warranty.md", "text": "Hardware warranty covers factory defects for 12 months. Water damage is not covered."},
    {"source": "hours.md", "text": "Customer support hours are Monday to Friday, 9 AM to 6 PM. Weekend emails get Monday replies."},
    {"source": "pickup.md", "text": "Store pickup is ready 2 hours after order confirmation. Bring photo ID to the front counter."},
    {"source": "payment.md", "text": "We accept Visa, Mastercard, and cash on delivery for orders. Gift cards never convert to cash."},
    {"source": "loyalty.md", "text": "Loyalty points earn 5 points per dollar on every order. Unused points expire after 12 months."},
]

eval_set = [
    {"id": "q1", "question": "How many days after purchase are refunds issued?", "expected_source": "refunds.md", "expected_facts": ["30 days"]},
    {"id": "q2", "question": "How long does standard shipping take?", "expected_source": "shipping.md", "expected_facts": ["5 business days"]},
    {"id": "q3", "question": "How long is hardware warranty for factory defects?", "expected_source": "warranty.md", "expected_facts": ["12 months"]},
    {"id": "q4", "question": "What are customer support hours on weekdays?", "expected_source": "hours.md", "expected_facts": ["Monday to Friday", "9 AM to 6 PM"]},
    {"id": "q5", "question": "Can I get fast money back on my laptop order?", "expected_source": "refunds.md", "expected_facts": ["30 days"]},
    {"id": "q6", "question": "Can I pay with crypto for online orders?", "expected_source": None, "expected_facts": []},
]


def content_words(text: str) -> list[str]:
    cleaned = re.sub(r"\[\d+\]", "", text.lower())
    return [w for w in re.findall(r"[a-z0-9]+", cleaned) if len(w) >= 4]


def score_answer(answer: str, expected_facts: list[str], context: str) -> dict:
    ans_low = answer.lower()
    if not expected_facts:
        facts = 1.0 if "i don't know" in ans_low else 0.0
    else:
        matched = sum(1 for f in expected_facts if f.lower() in ans_low)
        facts = matched / len(expected_facts)
    if "i don't know" in ans_low:
        return {"facts": facts, "faithful": True, "unsupported": []}
    ctx_words = set(content_words(context))
    unsupported: list[str] = []
    for word in content_words(answer):
        if word not in ctx_words and word not in unsupported:
            unsupported.append(word)
    return {"facts": facts, "faithful": len(unsupported) == 0, "unsupported": unsupported}


client = FakeLLM(embed_dim=256)
doc_matrix = np.array(client.embed([d["text"] for d in docs]), dtype=float)


def run_config(k: int) -> tuple[dict, list[dict]]:
    per_q = []
    for row in eval_set:
        q_vec = np.array(client.embed([row["question"]])[0], dtype=float)
        scores = doc_matrix @ q_vec
        order = np.argsort(-scores, kind="stable")[:k]
        hits = [docs[int(i)] for i in order]
        ctx = "\n".join(f"[{n}] {h['text']}" for n, h in enumerate(hits, 1))
        ans = client.chat([
            {"role": "system", "content": "Answer using only context.\n\nContext:\n" + ctx},
            {"role": "user", "content": row["question"]},
        ]).content or ""
        sc = score_answer(ans, row["expected_facts"], ctx)
        exp = row["expected_source"]
        hit = None if exp is None else (exp in [h["source"] for h in hits])
        per_q.append({"id": row["id"], "hit": hit, **sc})
    ans_rows = [r for r in per_q if r["hit"] is not None]
    idk_rows = [r for r in per_q if r["hit"] is None]
    summary = {
        "hits": sum(1 for r in ans_rows if r["hit"]),
        "n_ans": len(ans_rows),
        "facts_ok": sum(1 for r in ans_rows if r["facts"] == 1.0),
        "faithful": sum(1 for r in per_q if r["faithful"]),
        "n_all": len(per_q),
        "idk_ok": sum(1 for r in idk_rows if r["facts"] == 1.0),
        "n_idk": len(idk_rows),
    }
    return summary, per_q


print(f"{'config':<8} {'hit@k':<11} {'facts':<11} {'faithful':<11} {'idk'}")
runs = {}
for k in (1, 3):
    s, rows = run_config(k)
    runs[k] = rows
    h_str = f"{s['hits']}/{s['n_ans']} ({round(s['hits']/s['n_ans']*100)}%)"
    f_str = f"{s['facts_ok']}/{s['n_ans']} ({round(s['facts_ok']/s['n_ans']*100)}%)"
    g_str = f"{s['faithful']}/{s['n_all']} ({round(s['faithful']/s['n_all']*100)}%)"
    i_str = f"{s['idk_ok']}/{s['n_idk']} ({round(s['idk_ok']/s['n_idk']*100)}%)"
    print(f"k={k:<6} {h_str:<11} {f_str:<11} {g_str:<11} {i_str}")

print("Changed questions:")
for a, b in zip(runs[1], runs[3], strict=True):
    if (a["hit"], a["facts"]) != (b["hit"], b["facts"]):
        print(f"  {a['id']}: k=1(hit={a['hit']}, facts={a['facts']}) -> k=3(hit={b['hit']}, facts={b['facts']})")
