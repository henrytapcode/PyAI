A pipeline has several steps, and you want a log that shows when each step started and when it ended, even if the step crashes. The context manager `logged_step(log, name)` is already written, but three things are replaced by `___`. Replace each `___` so that the manager adds `"start <name>"` to the list `log` when the block starts, adds `"end <name>"` when the block ends, and gives the step name to `as`. Then press **Check**.

**Example**

| code | `log` afterwards |
|---|---|
| `with logged_step(log, "embed"): ...` | `["start embed", "end embed"]` |
| `with logged_step(log, "embed") as step: ...` | `step` is `"embed"` |

**Rules**
- `"start <name>"` is added **before** the body of the `with` runs.
- `"end <name>"` is added when the body ends, also when the body raises an error.
- An error raised in the body is not hidden: it still reaches the code around the `with`.
- Keep the `try` and `finally`; you only fill the blanks.
