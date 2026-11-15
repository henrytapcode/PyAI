# Retry with error feedback and fallback

**What it shows:** Sending validation errors back to the model in a copied message history so it can self-correct, and returning a safe fallback when all retries fail.

**Step by step**
1. Lines 16–32 define `validate_reply()` to collect missing keys and wrong-type errors against `TICKET_SCHEMA`.
2. Lines 35–58 define `get_structured()`, which copies `messages`, calls `client.chat()`, parses and validates the reply, and on error appends the bad reply plus error feedback before retrying.
3. Lines 62–76 run `get_structured()` twice: once with a script that fails once and recovers on attempt 2, and once with a script that fails three times and returns the `needs_review=True` fallback.

**Notice:** Copying `messages` at the start of `get_structured()` keeps the caller's original list clean across repeated retries.

**Try it yourself:** Raise `max_attempts=4` on Run 2 and add a fourth valid JSON reply to `failing_client`'s script to watch it recover instead of falling back.
