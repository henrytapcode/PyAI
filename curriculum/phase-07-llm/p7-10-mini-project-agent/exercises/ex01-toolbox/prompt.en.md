Implement the `ToolBox` class with methods `register`, `schemas`, `is_side_effect`, and `call` to manage an allowlisted set of agent tools. Write your code inside the class methods and `return` the required values.

**Example**

```python
box = ToolBox()
box.register(
    lambda order_id: {"id": order_id, "status": "delayed"},
    {
        "name": "lookup_order",
        "description": "Look up an order",
        "parameters": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
        },
    },
    side_effect=False,
)
print(box.is_side_effect("lookup_order"))            # False
print(box.call("lookup_order", {"order_id": "1042"}))  # {"id": "1042", "status": "delayed"}
print(box.call("unknown", {}))                        # error: unknown tool unknown
```

**Rules**

- `register(fn, schema: dict, side_effect: bool = False) -> None`:
  - Read the tool name from `schema["name"]`.
  - Raise `ValueError` if a tool with that name is already registered.
- `schemas() -> list[dict]`:
  - Return a list of tool schemas in registration order.
  - Return deep copies so mutating the returned list or any nested schema dict does not affect `ToolBox`.
- `is_side_effect(name: str) -> bool`:
  - Return `True` if `name` was registered with `side_effect=True`, else `False` (including unknown names).
- `call(name: str, args: dict) -> str`:
  - If `name` is not registered, return `f"error: unknown tool {name}"`.
  - Check `parameters.get("required", [])` in order; if a key is absent from `args` or its value is `None` or `""`, return `f"error: missing {key}"` for the first missing key.
  - Ignore any keys in `args` that are not listed in `parameters.get("properties", {})`, and never mutate the caller's `args` dictionary.
  - Call the registered function with the filtered keyword arguments inside `try/except`; on any `Exception as err`, return `f"error: {err}"`.
  - Serialize `dict` and `list` return values with `json.dumps()`, and convert all other return values with `str()`.
