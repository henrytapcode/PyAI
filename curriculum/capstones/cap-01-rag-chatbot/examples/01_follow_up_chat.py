# Simulate a 4-turn FAQ chat with follow-up rewriting and refusal.
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

client = FakeLLM(embed_dim=256)
chunks = [
    {"id": f"{d['source']}#{i}", "source": d["source"], "text": s.strip()}
    for d in docs
    for i, s in enumerate(re.split(r"(?<=[.!?])\s+", d["text"].strip()))
    if s.strip()
]
vecs = np.array(client.embed([c["text"] for c in chunks]), dtype=float)


def rewrite_query(question: str, history: list[dict]) -> str:
    prev_user = next((m["content"] for m in reversed(history) if m["role"] == "user"), "")
    if not prev_user:
        return question
    low = question.lower().strip()
    if len(question.split()) <= 4 or low.startswith(("what about", "and", "how about")):
        return f"{prev_user} {question}"
    return question


def ask_turn(question: str, history: list[dict], min_score: float = 0.2) -> dict:
    rewritten = rewrite_query(question, history)
    q_vec = np.array(client.embed([rewritten])[0], dtype=float)
    scores = vecs @ q_vec
    order = np.argsort(-scores, kind="stable")[:2]
    hits = [chunks[int(i)] for i in order if float(scores[int(i)]) >= min_score]
    if not hits:
        answer = "I don't know based on the provided context."
        sources: list[str] = []
    else:
        ctx = "\n".join(f"[{n}] {h['text']}" for n, h in enumerate(hits, 1))
        answer = client.chat([
            {"role": "system", "content": "Answer from context only.\n\nContext:\n" + ctx},
            {"role": "user", "content": rewritten},
        ]).content or ""
        sources = []
        if "i don't know" not in answer.lower():
            for raw in re.findall(r"\[(\d+)\]", answer):
                pos = int(raw) - 1
                if 0 <= pos < len(hits) and hits[pos]["source"] not in sources:
                    sources.append(hits[pos]["source"])
    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})
    return {"question": question, "rewritten": rewritten, "sources": sources, "answer": answer}


history: list[dict] = []
questions = [
    "How long are store pickup orders held?",
    "And photo ID?",
    "When do support agents work on weekdays?",
    "Do you offer cryptocurrency billing?",
]
for turn, q in enumerate(questions, 1):
    res = ask_turn(q, history)
    print(f"Turn {turn}:")
    print("  question :", res["question"])
    print("  rewritten:", res["rewritten"])
    print("  sources  :", res["sources"])
    print("  answer   :", res["answer"])
