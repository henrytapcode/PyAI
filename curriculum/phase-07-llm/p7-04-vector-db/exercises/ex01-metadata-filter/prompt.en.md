Complete `matches(metadata, where)` and `filter_indexes(metadatas, where)` in `starter.py` by replacing every `___` blank so records can be pre-filtered by metadata before top-k ranking.

Write your code inside the functions and `return` the boolean or list of matching integer indexes.

## Example

```python
matches({"lang": "vi", "topic": "faq"}, {"lang": "vi"})        # -> True
matches({"lang": "vi"}, {"lang": "vi", "topic": "faq"})        # -> False
filter_indexes([{"lang": "en"}, {"lang": "vi"}], {"lang": "vi"})  # -> [1]
```

## Rules

- If `where` is `None` or `{}` (empty), `matches()` returns `True` for every record.
- Every key/value pair in `where` must match; if a key is missing in `metadata`, return `False`.
- `filter_indexes()` must return matching indexes in their original ascending order.
