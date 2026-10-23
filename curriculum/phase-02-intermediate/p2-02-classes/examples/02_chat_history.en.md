# Chat history

**What it shows:** objects can hold other objects. A `ChatHistory` keeps a list of `ChatMessage` objects, and each message knows how to count its own words.

**Step by step**
1. Lines 2–11 define `ChatMessage` with two attributes, a `word_count` method and a `__repr__`.
2. Line 16 gives each `ChatHistory` its own empty list. Because it is created inside `__init__`, every history gets a separate list.
3. Lines 18–19 define `add`. It builds a `ChatMessage` and appends it to `self.messages`.
4. Lines 21–25 loop over the messages and ask each one for its `word_count()`. This is the accumulator pattern, now inside a method.
5. Lines 27–32 keep the text of the latest message with a given role, or `None` if there is none.
6. Line 40 prints the list. Each item in the list is shown with its `__repr__`.

**Notice:** `history.messages` is a plain list. A class does not hide it; it just keeps it together with the methods that work on it.

**Try it yourself:** add `history.add("assistant", "An object is one thing built from a class.")` before the prints. `words:` should grow and `last_text("assistant")` should return the new text.
