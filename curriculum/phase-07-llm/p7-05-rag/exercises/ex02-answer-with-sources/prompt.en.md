Implement `answer_with_sources(question, chunks, client, k=2, min_score=0.2)` in `starter.py` to retrieve top-`k` chunks, build a grounded prompt, call `client.chat()`, and return verified cited sources.

Write your code inside the function and `return` a dictionary `{"answer": str, "sources": list[str]}`.

## Example

```python
chunks = [
    {"text": "Refunds are issued within 30 days of purchase.", "source": "refunds.md"},
    {"text": "Standard shipping delivers in five days.", "source": "shipping.md"},
]
answer_with_sources("How many days do refunds take?", chunks, FakeLLM(embed_dim=256))
# -> {"answer": "Refunds are issued within 30 days of purchase. [1]", "sources": ["refunds.md"]}
```

## Rules

- Each element in `chunks` is `{"text": str, "source": str}`.
- Embed all chunk texts in one `client.embed(...)` call and embed `[question]` in a second call (two `embed` calls total; combining both into a single `embed` call is also accepted).
- Rank chunks by dot product (`doc_matrix @ q_vec`) using `np.argsort(-scores, kind="stable")[:k]`.
- If `chunks` is empty, `k <= 0`, or the top score is `< min_score`, return `{"answer": "I don't know.", "sources": []}` **without** calling `client.chat()`.
- Format the `system` message with instructions followed by a line equal to `Context:` and lines `[1] <text>`, `[2] <text>`, ... in top-`k` order, and pass `question` in a separate `user` message.
- Parse `[n]` citations in `answer`, ignore out-of-range numbers (`n < 1` or `n > len(hits)`), and map valid ones to `source` without duplicates, preserving order of first appearance.
