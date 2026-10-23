# Embedding timer

**What it shows:** a timer written with `@contextmanager` that records how long each fake embedding call takes, even when a call fails. The clock is a parameter, so the numbers are always the same.

**Step by step**
1. Lines 4–8 create a fake clock. Each call gives the next number from `ticks`, so no real time is involved.
2. Lines 11–17 define `timer`. It reads the clock, yields to the body, and in `finally` stores the label and the elapsed time in `results`.
3. Lines 26–32 time two successful calls. Each `with` reads the clock twice.
4. Lines 34–38 time a call that crashes: `len(None)` raises `TypeError`. The timing is still stored, then the error reaches `except`.
5. Lines 40–41 print every stored timing.

**Notice:** `broken batch: 0.2s` appears in the final list even though that call failed. That is the `try/finally` around `yield` at work.

**Try it yourself:** remove the `try:` and `finally:` lines in `timer` (and the extra indent). Run again: the failed call is no longer recorded.
