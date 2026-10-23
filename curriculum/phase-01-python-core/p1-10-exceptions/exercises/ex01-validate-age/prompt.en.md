Two functions are almost finished, but three words are missing. Replace every `___` with the right word (an error type or a value) so that bad ages raise a clear error and `age_or_none` turns bad input into `None`.

**Example**

| call | result |
|---|---|
| `validate_age(30)` | `30` |
| `validate_age(200)` | raises `ValueError("age must be between 0 and 120, got 200")` |
| `age_or_none("25")` | `25` |
| `age_or_none("x")` | `None` |
| `age_or_none("200")` | `None` |

**Rules**
- Fill the three blanks only; the `try`, `except` and `else` structure is already correct.
- An age from `0` to `120` (both included) is valid.
- `age_or_none` must not crash for any text: both `int("x")` and an age out of range raise `ValueError`.
- Press **Check** to run the tests.
