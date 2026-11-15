import json


def _dispatch_call(tc, registry: dict, required_map: dict[str, set[str]]) -> tuple[str, bool]:
    """Execute one tool call safely and return (result_str, did_run)."""
    fn = registry.get(tc.name)
    if fn is None:
        return f"error: unknown tool {tc.name}", False
    req = required_map.get(tc.name, set())
    clean_args = {
        key: val
        for key, val in tc.arguments.items()
        if key in req or val not in ("", None)
    }
    try:
        out = fn(**clean_args)
    except Exception as err:
        return f"error: {err}", True
    return (json.dumps(out) if isinstance(out, dict) else str(out)), True


def _assistant_tool_message(tool_calls) -> dict:
    return {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {"id": tc.id, "name": tc.name, "arguments": dict(tc.arguments)}
            for tc in tool_calls
        ],
    }


def run_with_tools(
    client,
    question: str,
    tools: list[dict],
    registry: dict,
    max_rounds: int = 3,
) -> tuple[str, list[str]]:
    """Run a bounded tool-calling loop by delegating dispatch to helper functions."""
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
        messages.append(_assistant_tool_message(resp.tool_calls))
        for tc in resp.tool_calls:
            content, did_run = _dispatch_call(tc, registry, required_map)
            if did_run:
                called.append(tc.name)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": content})

    return "stopped: too many tool calls", called
