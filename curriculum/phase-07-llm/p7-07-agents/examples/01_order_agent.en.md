# Order support agent with three read-only tools

**What it shows:** A bounded observe-think-act loop solving a multi-step order inquiry with `FakeLLM(script=...)` and recording a step-by-step trace.

**Step by step**
1. Lines 6–34 define three read-only local data tables (`ORDERS`, `DELIVERY_DAYS`, `POLICIES`) and their pure Python lookup functions.
2. Lines 37–57 register the three tool schemas in `TOOLS` and map their names to functions in `REGISTRY`.
3. Lines 60–84 implement `dispatch()` and `run_agent()`, looping up to `max_steps`, appending `assistant` (`tool_calls`) and `tool` messages, and recording each step in `trace`.
4. Lines 87–97 run a 3-step scripted task (`lookup_order` -> `estimate_delivery` -> final answer) and print the stop reason, trace lines, and final reply.

**Notice:** Each tool call appends both the `assistant` request and the `tool` observation before the next `chat()` call so the model sees what happened in the previous step.

**Try it yourself:** Change the second script item to `check_policy` with `{"status": "shipped"}` and watch the trace update without modifying `run_agent()`.
