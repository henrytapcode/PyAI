Implement `run_scenario(scenario, toolbox, make_client)` and `summarize(results)` to execute deterministic agent scenarios with safety limits and format a compact pass/fail summary. Write your code inside both functions and `return` the results.

**Example**

```python
res = run_scenario(scenario, toolbox, lambda script: FakeLLM(script=script))
# res -> {
#     "name": "happy_lookup",
#     "passed": True,
#     "stopped_reason": "final",
#     "tools": ["lookup_order"],
#     "reasons": [],
# }
print(summarize([res]))
# ["passed: 1/1", "all passed"]
```

**Rules**

- In `run_scenario(scenario: dict, toolbox, make_client) -> dict`:
  - Call `make_client(list(scenario["script"]))` once to create a fresh client for this scenario without mutating `scenario`.
  - Read `max_steps = scenario.get("max_steps", 6)`, `token_budget = scenario.get("token_budget")`, and `approve = scenario.get("approve")`.
  - On each step (`1 .. max_steps`), call `client.chat(messages, tools=toolbox.schemas())`, accumulate `resp.usage.total_tokens`, and check stop conditions in this exact order:
    1. `budget`: if `token_budget is not None` and cumulative tokens `> token_budget`, stop with `"budget"`.
    2. `final`: if `not resp.tool_calls`, capture `resp.content or ""` as the final answer and stop with `"final"`.
    3. `repeat`: take `tc = resp.tool_calls[0]` and `args = dict(tc.arguments)`; if the previous executed step had the exact same `(tool, args)`, stop with `"repeat"`.
    4. `needs_approval` / `rejected`: if `toolbox.is_side_effect(tc.name)` is `True`: when `approve is None`, stop immediately with `"needs_approval"`; otherwise call `approve(tc.name, dict(args))` and if it returns `False` (falsy), stop immediately with `"rejected"`. In both blocked cases, return without calling `toolbox.call(...)` and without adding `tc.name` to `tools`.
  - Otherwise execute `obs = toolbox.call(tc.name, dict(args))`, append the `assistant` (`content=None`, `tool_calls=[{"id": tc.id, "name": tc.name, "arguments": args}]`) and `tool` (`tool_call_id=tc.id`, `content=obs`) messages, and record `tc.name` in `tools`.
  - If all `max_steps` finish without stopping, set `stopped_reason = "max_steps"`.
  - Build `reasons: list[str]` in the fixed order `["stopped_reason", "tools", "answer"]`:
    - append `"stopped_reason"` if `stopped_reason != expect["stopped_reason"]`;
    - append `"tools"` if `tools != expect["tools"]`;
    - append `"answer"` if `expect.get("answer_contains")` is non-empty and not found case-insensitively in `answer`.
  - Return `{"name": scenario["name"], "passed": len(reasons) == 0, "stopped_reason": stopped_reason, "tools": tools, "reasons": reasons}`.
- In `summarize(results: list[dict]) -> list[str]`:
  - Start with `f"passed: {passed_count}/{len(results)}"`.
  - For every result where `not r["passed"]`, append `f"FAIL {r['name']}: {', '.join(r['reasons'])}"` in input order.
  - If there are zero failing results, append `"all passed"` at the end.
