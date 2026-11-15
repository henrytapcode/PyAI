Write `run_agent(client, task, tools, registry, max_steps=5, token_budget=None)` in `starter.py` to run a bounded multi-step agent loop with trace logging and stop conditions.

Write your code inside the function and `return` a result dictionary.

## Example

```python
run_agent(FakeLLM(script=script), "When will order 1042 arrive?", tools, registry)
# -> {
#     "answer": "Order 1042 arrives in 2 business days.",
#     "stopped_reason": "final",
#     "steps": 3,
#     "trace": [
#         {"step": 1, "tool": "lookup_order", "args": {"order_id": "1042"}, "observation": "shipped"},
#         {"step": 2, "tool": "estimate_delivery", "args": {"carrier": "FastPost"}, "observation": "2 business days"},
#     ],
# }
```

## Rules

- Return a dict with exact keys: `"answer"` (`str`, `""` when stopped early), `"stopped_reason"` (`"final"`, `"max_steps"`, `"repeat"`, or `"budget"`), `"steps"` (`int`, number of `client.chat` calls), and `"trace"` (list of `{"step", "tool", "args", "observation"}` dicts).
- Initialize `messages = [{"role": "user", "content": task}]` and loop for `step` from `1` to `max_steps`:
  - Call `resp = client.chat(messages, tools=tools)` and add `resp.usage.total_tokens` to the running token total.
  - Check stop conditions in this exact order:
    1. **budget**: if `token_budget is not None` and `total_tokens > token_budget`, return immediately with `stopped_reason="budget"`.
    2. **final**: if `not resp.tool_calls`, return immediately with `answer=resp.content or ""` and `stopped_reason="final"`.
    3. **repeat**: inspect the first tool call `tc = resp.tool_calls[0]` (`args = dict(tc.arguments)`). If `trace` is non-empty and the immediately preceding entry has the same `tool` and `args`, return immediately with `stopped_reason="repeat"` without running the tool.
  - Otherwise dispatch `tc` safely:
    - If `tc.name` is not in `registry`, observation is `f"error: unknown tool {tc.name}"`.
    - Else strip `""` / `None` from optional arguments (not in that tool's `"required"` schema list) and call `registry[tc.name](**clean_args)` inside `try/except Exception` (converting any exception to `f"error: {err}"`).
    - Serialize `dict` return values with `json.dumps(out)`, otherwise `str(out)`.
  - Append `{"role": "assistant", "content": None, "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": args}]}` and `{"role": "tool", "tool_call_id": tc.id, "content": observation}` to `messages`.
  - Append `{"step": step, "tool": tc.name, "args": args, "observation": observation}` to `trace`.
- If all `max_steps` finish without returning, return `stopped_reason="max_steps"` and `steps=max_steps`.
- Never mutate `tools` or `registry`.
