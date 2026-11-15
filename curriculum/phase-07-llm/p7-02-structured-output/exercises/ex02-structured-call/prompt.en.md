Implement `parse_reply(text)` and `get_ticket(client, messages, schema, max_attempts=3)` so your program can extract JSON from noisy replies and retry with error feedback before falling back to `None`.

Write your code inside the functions in `starter.py` (using the provided `_check_reply` helper) and `return` the required results.

## Example

```python
parse_reply('Sure!\n```json\n{"name": "Lan", "order_id": 1042}\n```')
# -> {"name": "Lan", "order_id": 1042}

client = FakeLLM(script=['{"name": "Lan"}', '{"name": "Lan", "order_id": 1042}'])
get_ticket(client, [{"role": "user", "content": "ticket"}], schema, max_attempts=3)
# -> ({"name": "Lan", "order_id": 1042}, 2)
```

## Rules

- `parse_reply(text)` slices from the first `"{"` to the last `"}"` and parses it with `json.loads()`.
- `parse_reply(text)` raises `ValueError` if `"{"` or `"}"` is missing, if JSON decoding fails, or if the parsed value is not a `dict`.
- `get_ticket(client, messages, schema, max_attempts=3)` calls `client.chat(..., response_format={"type": "json", "schema": schema})`, parses with `parse_reply`, and validates with `_check_reply`.
- If `parse_reply` raises `ValueError` or `_check_reply` returns errors, append an `"assistant"` message with the bad reply and a `"user"` message describing the error, then retry.
- Return `(data, attempt)` as soon as a valid reply is obtained, or `(None, max_attempts)` if all attempts fail.
- Never mutate the caller's original `messages` list.
