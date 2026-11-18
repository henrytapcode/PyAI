Build a FastAPI RAG service factory `create_app(docs, client, min_score=0.2) -> FastAPI`. Write your code inside `create_app` (and any Pydantic models or helpers you need) and return the configured `FastAPI` instance.

**Example**

```text
GET  /health                                           -> 200 {"status": "ok", "docs": 6}
GET  /documents/refunds                                -> 200 {"id": "refunds", "text": "Refunds take 5..."}
GET  /documents/missing                                -> 404 {"detail": "document not found"}
POST /ask {"question": "How long do refunds take?"}    -> 200 {"answer": "...", "sources": ["refunds", ...], "scores": [0.712, ...], "usage": {"prompt_tokens": ..., "completion_tokens": ...}}
POST /ask {"question": "Can I pay with crypto?"}       -> 200 {"answer": "I don't know based on the provided context.", "sources": [], "scores": [], "usage": {"prompt_tokens": 0, "completion_tokens": 0}}
POST /ask {"question": ""}                             -> 422
```

**Rules**
- Each item in `docs` is `{"id": str, "text": str}`. Call `client.embed([d["text"] for d in docs])` **once** inside `create_app` when creating the app.
- `GET /health` must return `{"status": "ok", "docs": len(docs)}`.
- `GET /documents/{doc_id}` returns `{"id": ..., "text": ...}` for a matching document, or raises `HTTPException(status_code=404, detail="document not found")`.
- `POST /ask` accepts JSON validated by Pydantic: `question` length `1..300`, `top_k` integer `1..5` with default `2`.
- Rank all `docs` by descending `cosine(q_vec, doc_vec)` (preserving original order on ties), take the top `top_k`, and drop any entry with `score < min_score`.
- If no hits remain, return `answer="I don't know based on the provided context."`, `sources=[]`, `scores=[]`, and `usage={"prompt_tokens": 0, "completion_tokens": 0}` **without calling `client.chat`**.
- Otherwise, call `client.chat` once with a message containing `Context:` followed by `[1] <text>`, `[2] <text>`... in `sources` order. If the model replies with the exact refusal `"I don't know based on the provided context."`, return `sources=[]` and `scores=[]`; otherwise return `[doc["id"] for doc in hits]` and `scores=[round(score, 3) ...]` in the same order, along with `usage` (`prompt_tokens`, `completion_tokens`).
- Keep all index state inside `create_app` (no module-level mutable state).
