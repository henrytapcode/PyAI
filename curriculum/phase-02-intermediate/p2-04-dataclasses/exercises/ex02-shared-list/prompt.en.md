The file below defines two dataclasses, but it has 3 bugs. `Chat` keeps a list of message texts, and `GenerationConfig` holds read-only settings for a model. Run the code, read the errors and fix the bugs until all tests pass. Change only the class definitions.

**Example**

```python
chat = Chat("demo")
chat.add("Hi")
print(chat.messages)     # ['Hi']
print(Chat("other").messages)   # []  (a new chat starts empty)

config = GenerationConfig("small", temperature=0.2)
print(config)            # GenerationConfig(model='small', temperature=0.2, max_tokens=256)
config.max_tokens = 1    # error: the config is read-only
```

**Rules**
- A new `Chat` starts with an empty `messages` list, and **every chat has its own list**.
- `Chat.add(text)` and `Chat.count()` already work. Do not change them.
- Messages can also be given when creating a chat: `Chat("demo", ["a", "b"])`.
- `GenerationConfig` has the fields `model` (required), `temperature` (default `0.7`) and `max_tokens` (default `256`), in this order.
- A `GenerationConfig` cannot be changed after it is built: assigning to any field raises an error.
