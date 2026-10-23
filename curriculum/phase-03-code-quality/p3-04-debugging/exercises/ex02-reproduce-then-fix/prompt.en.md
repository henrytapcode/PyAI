A teammate reports: "`last_n` sometimes returns too much." The function should return the last `n` items of a list, but one input gives a wrong answer. Work in two steps, like a real bug fix.

1. **Reproduce.** Find the smallest call that shows the bug. Make `reproduce()` return it as a tuple `(items, n)`. Try it by hand first (for example with **Visualize** or `print`).
2. **Fix.** Change `last_n` so that every case in the table is right.

**Example**

| call | result |
|---|---|
| `last_n([1, 2, 3, 4], 2)` | `[3, 4]` |
| `last_n([1, 2, 3], 10)` | `[1, 2, 3]` |
| `last_n([1, 2, 3, 4], 0)` | `[]` |
| `last_n([1, 2, 3], -1)` | raises `ValueError` |

**Rules**
- Write your code inside the two functions. `reproduce` must return a list and a number.
- The smallest failing input has exactly one item.
- Do not change the list you receive.
