Write `run_with_tools(client, question, tools, registry, max_rounds=3)` in `starter.py` to execute a bounded tool-calling loop with safe dispatch.

Write your code inside the function and `return` a `(final_answer, called)` tuple.

## Example

```python
run_with_tools(FakeLLM(), "What is the weather in Hanoi?", [weather_tool], {"get_weather": get_weather})
# -> ("Based on the tool result: 31C and sunny", ["get_weather"])

run_with_tools(FakeLLM(), "Tell me a joke", [weather_tool], {"get_weather": get_weather})
# -> ("(fake model) I received: Tell me a joke", [])
```

## Rules

- Start `messages` with `[{"role": "user", "content": question}]` and repeat at most `max_rounds` times:
  - Call `client.chat(messages, tools=tools)`.
  - If `resp.tool_calls` is empty, return `(resp.content or "", called)`.
  - Otherwise append `{"role": "assistant", "content": None, "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": dict(tc.arguments)} for tc in resp.tool_calls]}`.
  - For each `tc` in `resp.tool_calls`:
    - If `tc.name` is not in `registry`, use `f"error: unknown tool {tc.name}"`.
    - Otherwise append `tc.name` to `called`, strip `""` / `None` values from optional arguments (arguments not listed in that tool's `"required"` schema list), and call `registry[tc.name](**clean_args)` inside `try/except Exception` (turning any exception into `f"error: {err}"`).
    - Serialize `dict` return values with `json.dumps(out)`; convert non-string values with `str(out)`.
    - Append `{"role": "tool", "tool_call_id": tc.id, "content": result}` immediately after the `assistant` message.
- If all `max_rounds` finish without a final answer, return `("stopped: too many tool calls", called)`.
- Never mutate `tools` or `registry`.
