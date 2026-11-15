import json


def _dispatch(tc, registry: dict, required_map: dict[str, set[str]]) -> str:
    fn = registry.get(tc.name)
    if fn is None:
        return f"error: unknown tool {tc.name}"
    req = required_map.get(tc.name, set())
    clean_args = {
        k: v
        for k, v in tc.arguments.items()
        if k in req or v not in ("", None)
    }
    try:
        out = fn(**clean_args)
    except Exception as err:
        return f"error: {err}"
    return json.dumps(out) if isinstance(out, dict) else str(out)


def run_agent(
    client,
    task: str,
    tools: list[dict],
    registry: dict,
    max_steps: int = 5,
    token_budget: int | None = None,
) -> dict:
    """Run a bounded observe-think-act agent loop with trace and stop conditions."""
    required_map = {
        t["name"]: set(t.get("parameters", {}).get("required", []))
        for t in tools
    }
    messages = [{"role": "user", "content": task}]
    trace: list[dict] = []
    total_tokens = 0

    for step in range(1, max_steps + 1):
        resp = client.chat(messages, tools=tools)
        total_tokens += resp.usage.total_tokens
        if token_budget is not None and total_tokens > token_budget:
            return {
                "answer": "",
                "stopped_reason": "budget",
                "steps": step,
                "trace": trace,
            }
        if not resp.tool_calls:
            return {
                "answer": resp.content or "",
                "stopped_reason": "final",
                "steps": step,
                "trace": trace,
            }

        tc = resp.tool_calls[0]
        args = dict(tc.arguments)
        if trace and trace[-1]["tool"] == tc.name and trace[-1]["args"] == args:
            return {"answer": "", "stopped_reason": "repeat", "steps": step, "trace": trace}

        observation = _dispatch(tc, registry, required_map)
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": args}],
        })
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": observation})
        trace.append({"step": step, "tool": tc.name, "args": args, "observation": observation})

    return {"answer": "", "stopped_reason": "max_steps", "steps": max_steps, "trace": trace}
