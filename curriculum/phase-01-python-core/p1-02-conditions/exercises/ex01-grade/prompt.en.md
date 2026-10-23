Write the function `grade(score)` that turns a score (0 to 100) into a letter:

| Score | Grade |
|---|---|
| 90 or more | `"A"` |
| 80 to 89 | `"B"` |
| 70 to 79 | `"C"` |
| 60 to 69 | `"D"` |
| below 60 | `"F"` |

Write your code **inside the function** and use `return` to give back the answer. You will learn functions properly in lesson 5; for now just keep the `def` line and fill in the body.

Watch the boundaries: `90` is an `"A"`, `89` is a `"B"`.

**Example**

| Call | Returns |
|---|---|
| `grade(95)` | `"A"` |
| `grade(80)` | `"B"` |
| `grade(42)` | `"F"` |

**Rules**
- Return one of the strings `"A"`, `"B"`, `"C"`, `"D"`, `"F"`.
- The score is always a whole number from 0 to 100.
