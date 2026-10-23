# A helper that returns `None`

The `try/except` moves into a small function, `parse_score`, that returns the number or `None` after logging the warning. The main loop only keeps the results that are not `None`. Write `is not None` rather than a plain `if score:`, because the score `0` is a valid number that a plain `if` would throw away. This version is easier to read when the parsing rule grows (for example, "also accept `7/10`"). For a three-line rule the first solution is shorter.
