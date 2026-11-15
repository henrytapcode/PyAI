# Support assistant with token cost

**What it shows:** Sending a system message and three customer questions to `FakeLLM`, resending conversation history each turn, and estimating total cost from token usage.

**Step by step**
1. Lines 4–10 define hypothetical per-million-token prices, create `FakeLLM()`, and initialize `history` with a `system` message setting the assistant's tone.
2. Lines 11–15 list three customer questions, two matching built-in topics and one that triggers the fake model's echo fallback.
3. Lines 20–26 append each user question, call `client.chat(history)`, append the `assistant` reply to `history`, and accumulate `prompt_tokens` and `completion_tokens`.
4. Lines 28–38 print each turn's reply and token counts, then compute and print the grand total tokens (`223`) and hypothetical cost (`$0.000168`).

**Notice:** Even though each new question is short, `prompt_tokens` grows from `21` to `55` to `91` because the full conversation history is resent on every turn.

**Try it yourself:** Add a fourth question to `questions` and see how much `prompt_tokens` increases compared to Turn 1.
