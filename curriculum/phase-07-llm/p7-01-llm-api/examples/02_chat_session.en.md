# Stateful chat session class

**What it shows:** Wrapping `FakeLLM` inside a small `ChatSession` dataclass so callers only pass new text while `history` and `total_tokens` are maintained automatically.

**Step by step**
1. Lines 7–15 define `ChatSession` with `client`, `system`, `history`, and `total_tokens`, using `__post_init__` to insert the initial `system` message.
2. Lines 17–23 implement `ask(text)`, which appends the `user` message, calls `self.client.chat(self.history)`, appends the `assistant` reply, adds `resp.usage.total_tokens`, and returns the string reply.
3. Lines 26–34 run three questions through `session.ask(...)` and print the reply and growing `history` length (`3`, `5`, `7`) after each turn.
4. Lines 35–36 print the final history length (`7`) and total tokens (`208`).

**Notice:** Each turn adds two items to `history` (one `user` message and one `assistant` message), so three turns after the initial `system` message produce `1 + 2 * 3 = 7` messages.

**Try it yourself:** Pass `temperature=0.8` inside `self.client.chat(...)` with `FakeLLM(seed=3)` and verify that `ChatSession` still keeps the exact same history length.
