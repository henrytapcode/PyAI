Ruff would report several problems in this file, and three of them are real bugs. You cannot run ruff in the app, so read the code like a linter does. Fix the file so every test passes: remove what is unused, give `collect` a fresh list on every call, catch only the error that `parse_count` expects, and fix the typo in `total_length`. Change the code in place.

**Example**

| call | result |
|---|---|
| `collect("a")` then `collect("b")` | `["a"]` then `["b"]` |
| `parse_count("abc")` | `-1` |
| `parse_count(None)` | raises `TypeError` |
| `total_length(["ab", "c"])` | `3` |

**Rules**
- Remove the unused import.
- `collect` must not share a default list between calls. Use the `None` pattern from the lesson.
- `parse_count` must catch `ValueError` only, so other mistakes stay loud.
- `total_length` must add every text length to `total`.
