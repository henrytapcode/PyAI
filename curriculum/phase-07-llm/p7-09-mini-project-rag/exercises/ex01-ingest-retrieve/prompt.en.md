Write `build_index(docs, client, mode="sentence", size=8, overlap=2)` and `retrieve(index, question, client, k=2, min_score=0.2)` to ingest FAQ documents into a one-time embedding index and retrieve top-k matching chunks. Write your code inside both functions and `return` the results.

**Example**

```python
docs = [{"source": "refunds.md", "text": "Refunds take 30 days. Keep receipt!"}]
index = build_index(docs, client, mode="sentence")
# index["chunks"] -> [
#     {"id": "refunds.md#0", "source": "refunds.md", "text": "Refunds take 30 days."},
#     {"id": "refunds.md#1", "source": "refunds.md", "text": "Keep receipt!"},
# ]
hits = retrieve(index, "How many days for refunds?", client, k=2, min_score=0.2)
# hits[0] -> {"id": "refunds.md#0", "source": "refunds.md", "text": "Refunds take 30 days.", "score": ...}
```

**Rules**

- In `build_index`:
  - Accept only `mode="sentence"` or `mode="words"`; raise `ValueError` for any other `mode`.
  - Sentence split rule (`mode="sentence"`): strip `doc["text"]`; if non-empty, split on `r"(?<=[.!?])\s+"`, strip each piece, and drop empty pieces. For example, `"Refunds take 30 days. Keep receipt!"` splits into `["Refunds take 30 days.", "Keep receipt!"]`.
  - Word-window rule (`mode="words"`): raise `ValueError` if `size <= 0`, `overlap < 0`, or `overlap >= size`. Split with `.split()`, slide a window of `size` words advancing by `size - overlap`, and stop once `i + size >= len(words)`.
  - Skip empty documents/chunks and number each chunk ID as `f"{doc['source']}#{n}"` starting from `0` per source.
  - Call `client.embed(...)` **at most once** (exactly once for all non-empty chunks; zero calls if no chunks exist).
  - Return `{"chunks": chunks, "vectors": vectors}` without mutating `docs`.
- In `retrieve`:
  - Return `[]` immediately if `index["chunks"]` is empty or `k <= 0`.
  - Embed `[question]`, compute cosine/dot-product similarity against `index["vectors"]`, rank descending using stable ordering, take top `k`, and drop any chunk with `score < min_score`.
  - Return a list of dicts with keys `"id"`, `"source"`, `"text"`, and `"score"` rounded with `round(float(score), 3)`.
