# Answer direct, paraphrased, and unanswerable questions with citations.
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


def build_index(raw_docs: list[dict], client: FakeLLM) -> dict:
    chunks: list[dict] = []
    for doc in raw_docs:
        pieces = [s.strip() for s in re.split(r"(?<=[.!?])\s+", doc["text"].strip()) if s.strip()]
        for idx, text in enumerate(pieces):
            chunks.append({"id": f"{doc['source']}#{idx}", "source": doc["source"], "text": text})
    vectors = np.array(client.embed([c["text"] for c in chunks]), dtype=float)
    return {"chunks": chunks, "vectors": vectors}


def answer_with_sources(index: dict, question: str, client: FakeLLM, k: int = 2, min_score: float = 0.2) -> dict:
    q_vec = np.array(client.embed([question])[0], dtype=float)
    scores = index["vectors"] @ q_vec
    order = np.argsort(-scores, kind="stable")[:k]
    hits = [index["chunks"][int(i)] for i in order if float(scores[int(i)]) >= min_score]
    if not hits:
        return {"answer": "I don't know based on the provided context.", "sources": []}
    context = "\n".join(f"[{n}] {h['text']}" for n, h in enumerate(hits, 1))
    messages = [
        {
            "role": "system",
            "content": "Answer using only Context. Say I don't know if missing.\n\nContext:\n" + context,
        },
        {"role": "user", "content": question},
    ]
    answer = client.chat(messages).content or ""
    sources: list[str] = []
    if "i don't know" not in answer.lower():
        for raw in re.findall(r"\[(\d+)\]", answer):
            idx = int(raw) - 1
            if 0 <= idx < len(hits):
                src = hits[idx]["source"]
                if src not in sources:
                    sources.append(src)
    return {"answer": answer, "sources": sources}


client = FakeLLM(embed_dim=256)
index = build_index(docs, client)

queries = [
    ("direct", "How much does express delivery cost?"),
    ("paraphrase", "Can I get money back within a month?"),
    ("out_of_docs", "Do you offer cryptocurrency billing?"),
]
for kind, q in queries:
    res = answer_with_sources(index, q, client)
    print(f"[{kind}] {q}")
    print("  answer :", res["answer"])
    print("  sources:", res["sources"])
