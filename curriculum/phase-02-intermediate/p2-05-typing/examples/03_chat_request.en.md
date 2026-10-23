# A typed chat request

**What it shows:** a dataclass whose fields are type hints, including an optional `system` prompt, and a function that turns it into a list of messages.

**Step by step**
1. Lines 5–10 define `ChatRequest`. Each field has a hint. `system: str | None = None` means the field is optional and defaults to `None`.
2. Lines 13–18 take a `ChatRequest` and return `list[dict[str, str]]`.
3. Line 15 uses `is not None` (the opposite of `is None`) so the system message is added only when a system prompt exists.
4. Lines 21–22 build one request without a system prompt and one with it.
5. Lines 23–25 print the request and the two message lists.

**Notice:** the plain request has no `"system"` message at all, because `system` stayed `None`. Hints and defaults work together here.

**Try it yourself:** change the last argument of `careful` from `0.2` to `"hot"`. Python still runs it, because dataclass hints are not checked.
