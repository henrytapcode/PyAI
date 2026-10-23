# Flatten chats

**What it shows:** one comprehension with two `for` parts, used to pull every message out of a list of chats.

**Step by step**
1. Lines 2–6 hold three chats. Each chat is a list of messages, and some messages are empty or only spaces.
2. Line 8 has two `for` parts. Read them in order, like two nested loops: for each `chat` in `chats`, then for each `msg` in `chat`. That gives one flat list of 6 messages.
3. Line 11 adds a filter at the end. `msg.strip()` is an empty string for blank messages, and an empty string counts as `False`, so they are dropped. The kept messages are also stripped.
4. Line 14 builds a dict of message to length, but only for messages of 10 characters or fewer.

**Notice:** the `for` parts keep the **same order** as the loops you would write by hand: outer loop first, inner loop second.

**Try it yourself:** write the same thing as two nested `for` loops with `append`, and check that you get the same list.
