# Robust JSON reply parser

**What it shows:** Slicing out the JSON object from noisy LLM replies (markdown fences and prose lead-ins) and raising a clear `ValueError` when the reply is broken or lacks JSON.

**Step by step**
1. Lines 7–20 define `extract_json()`, which finds the first `{` and last `}`, parses the slice with `json.loads()`, and verifies the result is a `dict`.
2. Lines 23–29 prepare five scripted replies covering raw JSON, a fenced block, a chatty prefix, malformed JSON, and plain prose.
3. Lines 31–38 loop through all five replies from `FakeLLM(script=...)` and print either the parsed dictionary or the `ValueError` message.

**Notice:** Because `extract_json()` wraps `json.JSONDecodeError` and missing-brace checks into `ValueError`, callers only need one `except ValueError` handler.

**Try it yourself:** Add a sixth reply `'["not", "an", "object"]'` to `scripted_replies` and observe the error it produces.
