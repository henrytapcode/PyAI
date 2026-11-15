Implement `MiniStore` in `starter.py` so it supports batch upsert `add()`, pre-filtered top-k `search()` (including list-valued filters), `delete()`, and `len(store)`.

Write your code inside the class methods and `return` the requested values.

## Example

```python
client = FakeLLM(embed_dim=256)
store = MiniStore(client)
store.add(["c1", "c2"], ["cheap car rental", "fast laptop repair"], [{"lang": "en"}, {"lang": "vi"}])
store.search("affordable automobile", k=1, where={"lang": ["en", "vi"]})  # -> [("c1", 0.816)]
len(store)  # -> 2
```

## Rules

- `add(ids, texts, metadatas=None)` must call `client.embed(texts)` **once** per non-empty `add` call and default `metadatas` to `{}` per item when `None`.
- If an `id` already exists in the store, `add()` must **upsert** it (replace its text, metadata, and embedding vector without changing `len(store)`). If `ids` contains duplicate IDs within the same batch (or mismatches `texts`/`metadatas` lengths), raise `ValueError` without mutating the store.
- `search(query, k=3, where=None)` must pre-filter by `where` before taking top-k: if a filter value in `where` is a `list`, match records whose metadata value is in that list; otherwise match exact equality (`key in meta and meta[key] == val`). Return `(id, score)` tuples sorted by descending score (breaking ties by earlier insertion order), with each `score` rounded to 3 decimal places as a Python `float`.
- Return `[]` without error when the store is empty, `k <= 0`, or no record matches `where`.
- `delete(doc_id)` must remove both the record and its stored vector, or raise `KeyError` if `doc_id` is not found.
- `__len__()` must return the number of stored records.
