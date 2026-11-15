# Embed six shop FAQs once and match three customer questions using a threshold.
import numpy as np
from pyai_llm import FakeLLM

FAQS = [
    "Full refund available within 30 days.",
    "Fast laptop repair takes two days.",
    "Cheap car rental includes basic insurance.",
    "Free shipping on big orders over fifty dollars.",
    "Report checkout error to support team.",
    "Track package delivery with order number.",
]

QUERIES = [
    "Want full money back",
    "Quick computer repair",
    "Weather forecast tomorrow",
]

MIN_SCORE = 0.3

client = FakeLLM(embed_dim=256)
doc_matrix = np.array(client.embed(FAQS))

for query in QUERIES:
    q_vec = np.array(client.embed([query])[0])
    scores = doc_matrix @ q_vec
    best_idx = int(np.argsort(-scores, kind="stable")[0])
    best_score = round(float(scores[best_idx]), 3)
    if best_score < MIN_SCORE:
        print(f"Q: {query} -> no good match (score={best_score})")
    else:
        print(f"Q: {query} -> [{best_score}] {FAQS[best_idx]}")
