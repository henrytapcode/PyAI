Complete `check_reply(data, schema)` by replacing the `___` blanks in `starter.py` so it checks required keys, property types, and allowed `enum` values against a minimal JSON schema.

Write your code inside the function and `return` the list of error strings.

## Example

```python
schema = {
    "properties": {
        "name": {"type": "string"},
        "status": {"type": "string", "enum": ["open", "closed"]},
    },
    "required": ["name", "status"],
}
check_reply({"name": "Lan", "status": "pending"}, schema)
# -> ["status: must be one of ['open', 'closed']"]
```

## Rules

- Return `"missing: <key>"` for every key in `schema.get("required", [])` that is missing from `data`.
- Return `"wrong type: <key>"` for every key present in both `data` and `schema.get("properties", {})` whose value does not match its declared type.
- Support `"string"`, `"integer"`, `"number"`, and `"boolean"`, rejecting `bool` values (`True` / `False`) for `"integer"` and `"number"`.
- If a property spec has `"enum"` and the value passed its type check (if any) but is not in that list, append `f"{key}: must be one of {allowed}"` (e.g. `"status: must be one of ['open', 'closed']"`).
- Collect `"missing: ..."` errors first in `"required"` order, followed by `"wrong type: ..."` or `"<key>: must be one of ..."` errors in `"properties"` order.
- Do not report an error when a non-required property is omitted from `data`.
