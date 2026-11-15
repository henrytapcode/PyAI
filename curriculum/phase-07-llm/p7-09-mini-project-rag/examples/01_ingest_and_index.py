# Chunk FAQ docs with two strategies, index once, and retrieve top-k.
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


def chunk_docs(raw_docs: list[dict], mode: str, size: int = 8, overlap: int = 2) -> list[dict]:
    chunks: list[dict] = []
    for doc in raw_docs:
        if mode == "sentence":
            pieces = [s.strip() for s in re.split(r"(?<=[.!?])\s+", doc["text"].strip()) if s.strip()]
        else:
            words = doc["text"].split()
            step = size - overlap
            pieces = []
            i = 0
            while i < len(words):
                pieces.append(" ".join(words[i : i + size]))
                if i + size >= len(words):
                    break
                i += step
        for idx, text in enumerate(pieces):
            chunks.append({"id": f"{doc['source']}#{idx}", "source": doc["source"], "text": text})
    return chunks


sent_chunks = chunk_docs(docs, mode="sentence")
word_chunks = chunk_docs(docs, mode="words", size=8, overlap=2)
print("sentence:", len(sent_chunks), "ids:", [c["id"] for c in sent_chunks[:2]])
print("words   :", len(word_chunks), "ids:", [c["id"] for c in word_chunks[:2]])

client = FakeLLM(embed_dim=256)
vectors = np.array(client.embed([c["text"] for c in sent_chunks]), dtype=float)

question = "How long is hardware warranty for factory defects?"
q_vec = np.array(client.embed([question])[0], dtype=float)
scores = vectors @ q_vec
order = np.argsort(-scores, kind="stable")[:2]

print("Q:", question)
for rank, idx in enumerate(order, 1):
    chunk = sent_chunks[int(idx)]
    score = round(float(scores[int(idx)]), 3)
    print(f"#{rank} {chunk['id']} ({score}): {chunk['text'][:38]}")
