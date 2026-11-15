# Compare post-filter vs pre-filter on the same multilingual records.
import numpy as np
from pyai_llm import FakeLLM

RECORDS = [
    ("d1", "Full refund for broken laptop.", {"lang": "en"}),
    ("d2", "Fast money back for notebook.", {"lang": "en"}),
    ("d3", "Computer reimbursement policy.", {"lang": "en"}),
    ("d4", "Hoan tien refund cho laptop.", {"lang": "vi"}),
    ("d5", "Bao hanh computer trong 7 ngay.", {"lang": "vi"}),
    ("d6", "Thue xe cheap car theo ngay.", {"lang": "vi"}),
]

client = FakeLLM(embed_dim=256)
ids = [r[0] for r in RECORDS]
texts = [r[1] for r in RECORDS]
metadatas = [r[2] for r in RECORDS]
matrix = np.array(client.embed(texts), dtype=float)
q = np.array(client.embed(["money back for laptop"])[0], dtype=float)
k = 2
where = {"lang": "vi"}

# Post-filter: take top-k globally, then drop non-matching metadata
all_scores = matrix @ q
top_all = np.argsort(-all_scores, kind="stable")[:k]
post_hits = [
    (ids[int(i)], round(float(all_scores[int(i)]), 3))
    for i in top_all
    if metadatas[int(i)].get("lang") == where["lang"]
]

# Pre-filter: keep matching rows first, then take top-k
kept = [i for i, m in enumerate(metadatas) if m.get("lang") == where["lang"]]
sub_scores = matrix[kept] @ q
top_sub = np.argsort(-sub_scores, kind="stable")[:k]
pre_hits = [
    (ids[kept[int(j)]], round(float(sub_scores[int(j)]), 3))
    for j in top_sub
]

print("post-filter hits:", len(post_hits), post_hits)
print("pre-filter  hits:", len(pre_hits), pre_hits)
