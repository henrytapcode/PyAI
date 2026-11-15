Complete `is_repeat(history, name, args)` in `starter.py` by replacing each `___` blank so an agent can tell when it is repeating its immediately preceding tool call.

Write your code inside the function and `return` a `bool`.

## Example

```python
is_repeat([("lookup_order", {"order_id": "1042"})], "lookup_order", {"order_id": "1042"})
# -> True

is_repeat([("lookup_order", {"order_id": "1042"})], "lookup_order", {"order_id": "1043"})
# -> False
```

## Rules

- Return `False` when `history` is empty.
- Compare only against the **immediately preceding** step (`history[-1]`), not earlier steps.
- Return `True` only if both the tool `name` matches and `args` equals the previous argument dictionary (`==`).
- Never mutate `history` or `args`.
