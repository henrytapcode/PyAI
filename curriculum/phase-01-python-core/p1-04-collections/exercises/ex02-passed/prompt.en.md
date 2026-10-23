`passed(scores, threshold)` takes a dict of `name -> score` and returns a **sorted list of the names** whose score is **at least** `threshold`.

The code in the editor runs, but it has bugs. Find and fix them. Write your code inside the function and `return` the answer.

**Example**

| Call | Result |
|---|---|
| `passed({"Minh": 8, "Lan": 5, "Hoa": 3}, 5)` | `['Lan', 'Minh']` |
| `passed({"Lan": 1}, 5)` | `[]` |

**Rules**

- Return names only, not scores.
- A score equal to `threshold` counts as passed.
- The names come back in alphabetical order.

Press **Check** to run the tests.
