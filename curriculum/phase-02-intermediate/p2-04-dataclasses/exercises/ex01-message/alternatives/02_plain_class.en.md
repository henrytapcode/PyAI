# The same thing as a plain class

No dataclass here: `__init__`, `__repr__` and `__eq__` are all written by hand, and a missing `tags` is replaced inside `__init__` so each message gets its own list. (The `tags=None` trick is the usual way to avoid a shared default list in a plain class.) It passes the same tests, but it is about three times longer, which is exactly why dataclasses exist. Use a plain class only when the object needs real setup logic.
