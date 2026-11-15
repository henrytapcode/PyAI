# Deterministic scenario suite and summary report

**What it shows:** Executing seven scripted scenarios—covering happy path, error recovery, `repeat`, `max_steps`, approved refund, rejected refund, and `budget`—each with a fresh `FakeLLM` client, then printing a summary table and token report.

**Step by step**
1. Lines 5–42 set up the shop orders, tools, and schemas.
2. Lines 45–67 implement `run_agent()` checking `budget`, `final`, `repeat`, and side-effect approval in order.
3. Lines 75–158 define the seven `SCENARIOS` with golden `tools` trajectories and `answer_contains` checks.
4. Lines 160–198 run each scenario with its own `FakeLLM(script=...)`, print the `PASS`/`FAIL` table, and summarize counts by `stopped_reason` and total tokens.

**Notice:** Every scenario gets its own `FakeLLM(script=sc["script"])` instance inside the loop so scripts never exhaust early and `ToolCall.id` stays independent across scenarios.

**Try it yourself:** Swap the two entries in `happy_lookup`'s `expect["tools"]` list and run the script to see the exact `FAIL` row appear in the summary.
