Ruff prefers some forms over others: `is None` over `== None` (`E711`), `not in` over `not ... in` (`E713`), and `if flag:` over `if flag == True:` (`E712`). Each function below has a `___` where the idiom goes. Replace every `___` with the form ruff wants, using §7 of the lesson. The tests also check that your answer behaves correctly, not only that it looks right.

**Example**

| call | result |
|---|---|
| `describe(None)` | `"no data"` |
| `describe([1, 2])` | `"got 2 rows"` |
| `is_unknown("eggs", {"spam", "ham"})` | `True` |
| `switch_state("yes")` | `"on"` |

**Rules**
- Change only the three `___` blanks.
- Write a condition or an expression in each blank, not a whole statement.
