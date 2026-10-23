AI services fail now and then: a timeout, a busy server. Often the best answer is to simply try again. Write `retry(times)`, a decorator with an argument. A function decorated with `@retry(3)` is called up to 3 times until one call works. Write your code inside the function and `return` the decorator.

**Example**

```python
@retry(3)
def ask_llm(prompt):
    ...   # raises an error on the first two calls, returns "ok" on the third
```

| what happens inside | `ask_llm("hi")` |
|---|---|
| call 1 raises, call 2 raises, call 3 returns `"ok"` | returns `"ok"` |
| all 3 calls raise (the last error says `boom 3`) | raises the error that says `boom 3` |

**Rules**
- `times` is at least 1 and is the **total** number of attempts, so the first try counts.
- Return the result of the first call that works and stop. Do not call the function again.
- Any `Exception` counts as a failure and is tried again. If the last attempt also fails, raise the error of that last attempt.
- The exceptions lesson warns against a bare `except Exception:`. A retry wrapper is one of the few reasonable places for it, because it raises the error again at the end. Real code often retries only specific errors, such as `TimeoutError`.
- Pass all positional and keyword arguments on to the original function.
- The decorated function keeps its original name and docstring.
- Do not wait or sleep between attempts.
