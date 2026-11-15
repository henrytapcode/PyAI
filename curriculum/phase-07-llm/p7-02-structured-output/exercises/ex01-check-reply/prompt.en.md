Complete `check_reply(data, schema)` by replacing the `___` blanks in `starter.py` so it checks required keys and property types against a minimal JSON schema.

Write your code inside the function and `return` the list of error strings.

## Example

```python
schema = {
    "properties": {"name": {"type": "string"}, "order_id": {"type": "integer"}},
    "required": ["name", "order_id"],
}
check_reply({"name": "Lan", "order_id": True}, schema)
# -> ["wrong type: order_id"]
```

## Rules

- Return `"missing: <key>"` for every key in `schema.get("required", [])` that is missing from `data`.
- Return `"wrong type: <key>"` for every key present in both `data` and `schema.get("properties", {})` whose value does not match its declared type.
- Support `"string"`, `"integer"`, `"number"`, and `"boolean"`.
- Reject `bool` values (`True` / `False`) for `"integer"` and `"number"`.
- Accept both `int` and `float` (excluding `bool`) for `"number"`.
- Do not report an error when a non-required property is omitted from `data`.
