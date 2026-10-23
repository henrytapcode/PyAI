# Timing an embedding step

**What it shows:** a `timed` decorator that measures a function and stores the time in a dict, without printing and without changing what the function returns.

**Step by step**
1. Line 5 creates the dict `timings`. The wrapper will fill it.
2. Lines 8–16 define `timed`. The wrapper reads the stopwatch, calls the original function with all its arguments, reads the stopwatch again, and saves the difference under the function's name.
3. Line 9 puts `@wraps(func)` on the wrapper, so the decorated function keeps its name and docstring.
4. Lines 19–22 decorate `embed`, a fake embedding step that turns each text into `[length, number of words]`.
5. Line 25 calls `embed` normally. Lines 26–29 print the vectors, the name, the keys of `timings`, and a check that the time is not negative.

**Notice:** the exact time is never printed, because it changes on every run. Print only what is stable, and test the rest with a comparison such as `>= 0`.

**Try it yourself:** call `embed(["a", "b", "c"])` a second time before the prints. The dict still has one key, because the new time replaces the old one under the same name.
