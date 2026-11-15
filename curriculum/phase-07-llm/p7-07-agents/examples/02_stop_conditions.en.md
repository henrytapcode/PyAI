# Four agent stop conditions

**What it shows:** One `run_agent()` implementation stopping cleanly for four distinct reasons—`final`, `max_steps`, `repeat`, and `budget`—under four different `FakeLLM` scripts.

**Step by step**
1. Lines 33–60 implement `run_agent()` with four brakes: a `for` loop capped at `max_steps`, cumulative `total_tokens` checked against `token_budget`, an early return when `tool_calls` is empty, and a repeat check comparing against `trace[-1]`.
2. Lines 63–101 define four scripted scenarios: a normal 2-step completion, alternating tools that exceed `max_steps=3`, an identical repeated tool call on step 2, and a tight `token_budget=25`.
3. Lines 103–105 run each scenario with a fresh `FakeLLM(script=script)` and print `stopped_reason`, `steps`, and `tokens`.

**Notice:** Checking `token_budget` right after `client.chat()` and checking `repeat` before running the tool prevents wasted tool calls and keeps step counts exact.

**Try it yourself:** Raise `token_budget` in the fourth scenario from `25` to `100` and confirm `stopped_reason` switches from `budget` to `final`.
