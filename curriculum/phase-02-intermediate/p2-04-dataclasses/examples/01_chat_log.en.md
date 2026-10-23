# Chat log

**What it shows:** a dataclass with a method and a list field, used the way chat APIs expect: a list of messages that becomes a list of dicts.

**Step by step**
1. Lines 6–10 define `Message` with two required fields and a `tags` list that starts empty for every message.
2. Lines 12–13 add a normal method, `word_count`. It uses `self` exactly like in a plain class.
3. Lines 16–20 build three messages. The second one passes `tags=["question"]`; the others use the default empty list.
4. Lines 22–25 are the accumulator pattern again: add each message's word count to `total_words` and print the message. The printout comes from the `__repr__` that `@dataclass` wrote.
5. Line 28 compares a message from the list with a brand-new one. They are different objects but hold the same data, so `==` gives `True`.
6. Lines 30–33 turn each message into a dict with `asdict`, then show one as JSON text.

**Notice:** the `tags` of the first message is `[]`, and it is not shared with the others. Each message got its own list from `default_factory`.

**Try it yourself:** add a field `name: str = ""` after `tags` and run again. Every printed message shows the new field, and you did not touch any `__repr__`.
