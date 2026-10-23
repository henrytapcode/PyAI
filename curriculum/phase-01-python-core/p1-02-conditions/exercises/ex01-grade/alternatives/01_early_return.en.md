# Separate `if`s with early `return`

Here every check is its own `if`, with no `elif` and no `else`. It still works because `return` leaves the function at once: when `score` is 85, the `return "B"` line ends the function and the later checks never run. Use `elif` when you want the chain to be visible at a glance; use early returns when each branch simply hands back an answer.
