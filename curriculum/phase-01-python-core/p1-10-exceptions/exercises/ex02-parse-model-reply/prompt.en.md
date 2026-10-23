A classifier model should answer with JSON like `{"label": "spam", "score": 0.9}`, but real replies are sometimes broken. Write `parse_reply(text)` so it never crashes: it returns the parsed `label` and `score`, or a safe "unknown" result. Then write `count_unknown(replies)`. Write your code inside the functions and `return` the answer.

**Example**

| input | result |
|---|---|
| `'{"label": "spam", "score": 0.9}'` | `{"label": "spam", "score": 0.9}` |
| `"Sure! Here is the JSON"` | `{"label": "unknown", "score": 0.0}` |
| `'{"label": "ham"}'` | `{"label": "unknown", "score": 0.0}` |
| `'{"label": "ham", "score": 1.5}'` | `{"label": "unknown", "score": 0.0}` |

**Rules**
- Use `json.loads` (the `json` module is already imported in the starter).
- The fallback is used for invalid JSON, a missing `"label"` or `"score"`, JSON that is not a dict (like a list), a score that is not a number, and a score below `0` or above `1`.
- `0` and `1` are valid scores.
- `count_unknown(replies)` returns how many replies in the list give the unknown result.
- Do not use a bare `except:`. Name the error types.
