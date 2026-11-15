# Compare keyword overlap and cosine similarity across three queries and four docs.
import numpy as np
from pyai_llm import FakeLLM

DOCS = [
    "Cheap car rental today",
    "Fast laptop repair shop",
    "Quick refund for error",
    "Friendly clinic doctor",
]

QUERIES = [
    "affordable automobile",
    "rapid computer",
    "reimbursement bug",
]


def keyword_hits(query: str, doc: str) -> int:
    return len(set(query.lower().split()) & set(doc.lower().split()))


client = FakeLLM(embed_dim=256)
doc_matrix = np.array(client.embed(DOCS))

print(f"{'query':<22} {'doc':<5} {'kw':>2} {'cos':>6}")
print("-" * 38)
for query in QUERIES:
    q_vec = np.array(client.embed([query])[0])
    scores = doc_matrix @ q_vec
    for idx, doc in enumerate(DOCS):
        kw = keyword_hits(query, doc)
        cos = round(float(scores[idx]), 3)
        print(f"{query:<22} doc{idx:<2} {kw:>2} {cos:>6.3f}")
