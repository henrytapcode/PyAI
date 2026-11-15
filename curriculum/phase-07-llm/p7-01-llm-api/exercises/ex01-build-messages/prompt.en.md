Fill in the `___` blanks inside `build_messages(system, history, user)` so it returns the full list of message dictionaries ready for `FakeLLM().chat(...)`.

Each item in `history` is a `(user_text, assistant_text)` tuple representing one past turn. Write your code inside the function and `return` the list.

**Example**

```python
build_messages("Be concise.", [("Hi", "Hello!")], "What is RAG?")
# [
#     {"role": "system", "content": "Be concise."},
#     {"role": "user", "content": "Hi"},
#     {"role": "assistant", "content": "Hello!"},
#     {"role": "user", "content": "What is RAG?"},
# ]
```

**Rules**

- Start with one `"system"` message, then each `(user, assistant)` pair from `history` as two messages, then the new `"user"` message.
- Work cleanly when `history` is empty (`[]`).
- Do not modify `history` in place.
