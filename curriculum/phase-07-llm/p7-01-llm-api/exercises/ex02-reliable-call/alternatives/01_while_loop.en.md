# Retry loop with `while` instead of `for`

This alternative tracks the attempt counter explicitly in a `while attempt <= max_attempts:` loop instead of `for attempt in range(1, max_attempts + 1):`.

Both versions behave identically when `RateLimitError` occurs and re-raise on the final attempt. A `for` loop with `range` is usually safer because you cannot forget `attempt += 1`, whereas a `while` loop is handy when the retry budget or delay rule changes dynamically mid-loop.
