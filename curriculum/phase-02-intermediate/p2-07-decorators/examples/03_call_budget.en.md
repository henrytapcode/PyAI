# A call budget for an LLM

**What it shows:** a decorator with an argument. `@limit_calls(2)` lets a function run twice and then refuses, which protects you from an accidental loop that spends your money.

**Step by step**
1. Lines 5–16 have three levels: `limit_calls(max_calls)` returns `decorator`, which returns `wrapper`.
2. Line 7 creates the list `used` once per decorated function. Each allowed call adds one item to it, so `len(used)` is the number of calls so far.
3. Lines 11–12 check the budget **before** calling the function, and `raise` a `RuntimeError` when it is used up.
4. Lines 19–21 decorate `ask_llm`, a stub that returns a fixed text instead of calling a real API.
5. Lines 24–25 use up the budget. Lines 26–29 try a third time and catch the error with `try` / `except`.

**Notice:** line 19 has brackets: `@limit_calls(2)`. The `2` is the setting, and it travels in the backpack of `wrapper` as `max_calls`.

**Try it yourself:** change `@limit_calls(2)` to `@limit_calls(3)`. The third call should now succeed and nothing should be blocked.
