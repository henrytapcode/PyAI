# Separate except blocks and an early return

This version lists `json.JSONDecodeError` in its own `except` block and handles `KeyError` and `TypeError` in another. It checks the score range with an early `return` instead of `raise`. It uses a shared `UNKNOWN` dict and `sum(...)` with a generator, a short form you will meet later in the course. Separate blocks are the better choice when you want to react differently to each problem, for example print a different message. When every error gets the same fallback, one tuple (as in the main solution) is shorter.
