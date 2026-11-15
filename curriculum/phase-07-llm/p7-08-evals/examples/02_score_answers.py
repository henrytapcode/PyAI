# Run full RAG answers on the eval set and test a scripted hallucination.
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

print(f"{'id':<4} {'facts':<7} {'faithful':<10} {'idk'}")
q1_context = ""
for row in eval_set:
    q_vec = np.array(client.embed([row["question"]])[0], dtype=float)
    scores = doc_matrix @ q_vec
    order = np.argsort(-scores, kind="stable")[:2]
    hits = [docs[int(i)] for i in order]
    ctx = "\n".join(f"[{n}] {h['text']}" for n, h in enumerate(hits, 1))
    if row["id"] == "q1":
        q1_context = ctx
    ans = client.chat([
        {"role": "system", "content": "Answer using only context.\n\nContext:\n" + ctx},
        {"role": "user", "content": row["question"]},
    ]).content or ""
    sc = score_answer(ans, row["expected_facts"], ctx)
    is_idk = "i don't know" in ans.lower()
    print(f"{row['id']:<4} {sc['facts']:<7} {str(sc['faithful']):<10} {is_idk}")

# Script simulates a model that includes the fact yet fabricates extra claims.
fake_client = FakeLLM(script=["Refunds are issued within 30 days with free courier pickup. [1]"])
hallucinated = fake_client.chat([
    {"role": "system", "content": "Context:\n" + q1_context},
    {"role": "user", "content": eval_set[0]["question"]},
]).content or ""
bad_score = score_answer(hallucinated, eval_set[0]["expected_facts"], q1_context)
print(f"scripted: facts={bad_score['facts']} faithful={bad_score['faithful']}")
print("unsupported:", bad_score["unsupported"])
