# Retrying transient errors with exponential backoff

**What it shows:** Wrapping `client.chat(...)` in a `for` loop that catches `RateLimitError`, prints doubling wait times (`0.5s`, `1.0s`, `2.0s`), and re-raises if all attempts fail.

**Step by step**
1. Lines 5–19 define `call_with_retry(client, messages, max_attempts=3)` using a `for` loop from `1` to `max_attempts`.
2. Lines 10–14 call `client.chat(messages)` inside `try` and return `resp.content` immediately if no exception occurs.
3. Lines 15–19 catch `RateLimitError`, compute the simulated exponential backoff `0.5 * 2 ** (attempt - 1)`, print the wait duration instead of sleeping, and re-raise on the final attempt.
4. Lines 24–33 demonstrate both outcomes: `FakeLLM(fail_times=2)` recovers on attempt 3, while `FakeLLM(fail_times=5)` exhausts all 3 attempts and lets `RateLimitError` propagate to the caller's `except` block.

**Notice:** Checking `if attempt == max_attempts: raise` ensures you never swallow the final failure silently.

**Try it yourself:** Change `max_attempts=3` to `max_attempts=6` in Case 2 and watch `FakeLLM(fail_times=5)` succeed on attempt 6.
