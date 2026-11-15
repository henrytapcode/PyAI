Implement `top_k(query, docs, client, k=2, min_score=0.0)` in `starter.py` to rank documents by embedding similarity and filter out weak matches.

Write your code inside the function and `return` the list of `(index, score)` tuples.

## Example

```python
client = FakeLLM(embed_dim=256)
docs = ["cheap car rental", "fast laptop repair", "book a doctor"]
top_k("affordable automobile", docs, client, k=1, min_score=0.3)
# -> [(0, 0.816)]
```

## Rules

- If `docs` is empty (or `k <= 0`), return `[]` immediately **without** calling `client.embed(...)`.
- Embed `docs` in a single batch call (either `client.embed(docs)` plus `client.embed([query])`, or one combined call `client.embed([query, *docs])` — never call `embed` once per document in a loop).
- Return `(index, score)` pairs sorted by descending score; break ties by placing smaller `index` first.
- Round each `score` to 3 decimal places as a plain Python `float` (never a NumPy scalar).
- Exclude any document whose score is strictly less than `min_score`.
- If `k` is larger than the number of documents, return all qualifying documents.
