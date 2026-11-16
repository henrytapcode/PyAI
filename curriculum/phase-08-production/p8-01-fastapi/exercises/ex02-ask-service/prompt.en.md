Build a small document-lookup FastAPI service using the starter `app`, `DOCS` dictionary, and `AskRequest` skeleton. Write your code inside `AskRequest`, `health()`, and `ask()`, returning the response dictionaries directly from the route functions.

**Example**

```text
GET  /health                                       -> 200 {"status": "ok"}
POST /ask {"question": "FastAPI tests"}            -> 200 {"question": "FastAPI tests", "sources": [3, 4]}
POST /ask {"question": "FastAPI tests", "top_k": 5}-> 200 {"question": "FastAPI tests", "sources": [3, 4, 1]}
POST /ask {"question": "unknown topic"}            -> 404 {"detail": "no matching documents"}
POST /ask {"question": ""}                         -> 422
```

**Rules**
- Constrain `AskRequest` with `Field(...)`: `question` length `1..200`, and `top_k` integer `1..5` with default `2`.
- `GET /health` must return `{"status": "ok"}`.
- In `POST /ask`, compare words using lowercase whitespace splitting (`text.lower().split()`), keep doc IDs with at least `1` shared word, sort by shared word count descending then `doc_id` ascending, and keep at most `top_k` IDs.
- If zero documents match, raise `HTTPException(status_code=404, detail="no matching documents")`.
