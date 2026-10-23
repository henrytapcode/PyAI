The function `check_reply` decides if a model reply is usable and writes what happened to the log. The messages are already written, but each `logger.___(...)` has a blank where the level goes. Replace every `___` with the right logging method: `debug`, `info`, `warning`, `error` or `critical`. Pick each one from the comment next to it and the level table in §2.

**Example**

| call | returns | logs |
|---|---|---|
| `check_reply("hello", 1)` | `True` | one `DEBUG` record: `reply has 5 characters` |
| `check_reply("", 1)` | `False` | one `WARNING` record: `empty reply, retrying (attempt 1)` |
| `check_reply("", 3)` | `False` | one `ERROR` record: `giving up after 3 attempts` |

**Rules**
- Change only the three blanks. The messages and the `return` lines are already correct.
- The tests read the log with `caplog`, so the level of each record is checked.
