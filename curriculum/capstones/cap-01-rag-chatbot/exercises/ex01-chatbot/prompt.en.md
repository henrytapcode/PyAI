Implement the stateful `ChatBot` class (`__init__` and `ask`) using the provided `build_index` and `retrieve` helpers in `starter.py`. Unlike the standalone snippets in the lesson, your class must bundle all steps into per-instance state, keep the `system` prompt pinned outside `history` during trimming, refuse out-of-scope queries without calling `client.chat`, filter only valid `[n]` citations, and rewrite follow-ups from the original user question rather than an already-rewritten query. Write your code inside `ChatBot` and `return` the result dictionary from `ask`.

**Example**

```python
bot = ChatBot(docs, client)

bot.ask("How long are store pickup orders held?")
# -> {
#     "answer": "Unclaimed orders are held at the counter for 7 days. [2]",
#     "sources": ["pickup.md"],
#     "rewritten": "How long are store pickup orders held?",
# }

bot.ask("And photo ID?")
# -> {
#     "answer": "Bring a photo ID at pickup. [1]",
#     "sources": ["pickup.md"],
#     "rewritten": "How long are store pickup orders held? And photo ID?",
# }

bot.ask("Do you offer cryptocurrency billing?")
# -> {
#     "answer": "I don't know based on the provided context.",
#     "sources": [],
#     "rewritten": "Do you offer cryptocurrency billing?",
# }
```

**Rules**

- Keep the module constants `REFUSAL = "I don't know based on the provided context."` and `DEFAULT_SYSTEM = "Answer only from the shop FAQ context and cite sources as [n]."`, and match the signature `ChatBot(docs, client, system_prompt=DEFAULT_SYSTEM, k=2, min_score=0.2, max_history_tokens=60)`.
- In `__init__`, call `build_index(docs, client)` **once** so chunks are embedded once for the lifetime of the bot, and give every `ChatBot` instance its own `self.history: list[dict]` (only `{"role": "user"|"assistant", "content": ...}` turns, never `system`).
- In `ask(question)`: strip `question` and raise `ValueError` if it is empty or whitespace-only.
- **Follow-up rewriting:** find the most recent `"user"` message in `self.history` (the original question typed by the user, not the rewritten text). If one exists and the new question has `<= 4` words, has `"and"` as its lowercased first word, or starts with `"what about "` or `"how about "` (case-insensitive), set `rewritten = f"{prev_user} {question}"`; otherwise `rewritten = question`.
- Call `retrieve(self.index, rewritten, self.client, self.k, self.min_score)`. If there are no hits, set `answer = REFUSAL` and `sources = []` **without calling `client.chat`**.
- If there are hits, call `client.chat` **once** with `temperature=0.0` and `messages = [{"role": "system", "content": system_prompt + "\n\nContext:\n[1] <text>\n[2] <text>..."}, *self.history, {"role": "user", "content": rewritten}]`.
- **Citations:** find every `[n]` in `answer`, keep only indices where `1 <= n <= len(hits)`, and collect unique `hit["source"]` values in order of appearance into `sources`. Return `answer` verbatim.
- **History & trimming:** after every `ask` (including refusals), append `{"role": "user", "content": question}` and then `{"role": "assistant", "content": answer}` to `self.history`. While `count_tokens(system_prompt) + sum(count_tokens(m["content"]) for m in self.history) > max_history_tokens` and `len(self.history) > 2`, drop the oldest turn (`self.history.pop(0)`). The `system` prompt is never dropped, and the latest pair of turns is always kept.
