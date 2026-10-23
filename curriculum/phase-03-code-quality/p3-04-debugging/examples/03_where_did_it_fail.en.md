# Where did it fail?

**What it shows:** a program catches an error and reports the same facts you read from a traceback: the error type, the message, and the chain of calls that led to it.

**Step by step**
1. Lines 5–6 define `parse_score`, which calls `int(text)` and can raise `ValueError`.
2. Lines 9–13 define `load_scores`, which calls `parse_score` for each line in a `for` loop.
3. Inside `main`, line 18 calls `load_scores` with the middle value `"abc"` that cannot be a number.
4. Line 20 asks the `traceback` module for the frames of the error. `err.__traceback__` holds the chain of calls, and `traceback.extract_tb` turns it into a list of frames. Each frame has a `name`.
5. The output shows the type and message first, then the path `main -> load_scores -> parse_score`. This is the same story as a printed traceback, but from top to bottom.

**Notice:** the last name in the path, `parse_score`, is where the error was raised. The real question is why `load_scores` sent it `"abc"`.

**Try it yourself:** change `"abc"` to `"5"`. The `except` branch does not run, so nothing is printed.
