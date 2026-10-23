A teacher exports exam scores as text, and some lines are broken. Write `load_scores(raw_scores)`. It takes a list of strings, converts each one to an `int`, and returns the list of numbers. It also **logs what happened**, so that someone reading the log can see which lines were skipped. Write your code inside the function and `return` the answer.

**Example**

| call | returns | log records |
|---|---|---|
| `load_scores(["10", "7"])` | `[10, 7]` | `INFO` `loaded 2 of 2 scores` |
| `load_scores(["10", "abc", "7"])` | `[10, 7]` | `WARNING` `skipping bad score: abc`, then `INFO` `loaded 2 of 3 scores` |
| `load_scores([])` | `[]` | `INFO` `loaded 0 of 0 scores` |

**Rules**
- A text that `int()` cannot convert (it raises `ValueError`) is skipped. Log **one** record at `WARNING` level for it, with exactly the message `skipping bad score: <text>`, where `<text>` is the original string.
- After the loop, log **one** record at `INFO` level, with exactly the message `loaded <n> of <total> scores`, where `<n>` is the number of good scores and `<total>` is the length of `raw_scores`.
- Do not log anything else, and do not use `print`.
- The good scores keep their original order.
- Use the module-level `logger` that is already in the starter code.
