import json


def run_with_tools(
    client,
    question: str,
    tools: list[dict],
    registry: dict,
    max_rounds: int = 3,
) -> tuple[str, list[str]]:
    """Run a bounded tool-calling loop and return (final_answer, called_tool_names).

    Example:
        run_with_tools(FakeLLM(), "What is the weather in Hanoi?", tools, registry)
        -> ("Based on the tool result: 31C and sunny", ["get_weather"])
    """
    required_map = {
        t["name"]: set(t.get("parameters", {}).get("required", []))
        for t in tools
    }
    messages = [{"role": "user", "content": question}]
    called: list[str] = []

    for _ in range(max_rounds):
        resp = client.chat(messages, tools=tools)
        if not resp.tool_calls:
            return resp.content or "", called

        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {"id": tc.id, "name": tc.name, "arguments": dict(tc.arguments)}
                for tc in resp.tool_calls
            ],
        })
        for tc in resp.tool_calls:
            if tc.name not in registry:
                result = f"error: unknown tool {tc.name}"
            else:
                called.append(tc.name)
                req = required_map.get(tc.name, set())
                clean_args = {
                    k: v
                    for k, v in tc.arguments.items()
                    if k in req or v not in ("", None)
                }
                try:
                    out = registry[tc.name](**clean_args)
                except Exception as err:
                    result = f"error: {err}"
                else:
                    result = json.dumps(out) if isinstance(out, dict) else str(out)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result,
            })

    return "stopped: too many tool calls", called
