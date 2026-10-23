Write `report_line(model, tokens, cost)` that returns one line of a usage table. The model name is left-aligned in 12 characters, the token count is right-aligned in 10 characters with commas, and the cost is right-aligned in 8 characters with 2 decimals.

**Example**

| call | returns |
|---|---|
| `report_line("small", 12345, 3.5)` | `"small           12,345    3.50"` |
| `report_line("big", 987, 0.126)` | `"big                987    0.13"` |

**Rules**
- Write your code inside the function and `return` the string (do not `print` it).
- Use one f-string with format specs. Press **Check** to run the tests.
