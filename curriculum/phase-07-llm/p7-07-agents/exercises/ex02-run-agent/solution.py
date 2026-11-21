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


def _agent_result(reason: str, steps: int, trace: list[dict], answer: str = "") -> dict:
    return {
        "answer": answer,
        "stopped_reason": reason,
        "steps": steps,
        "trace": trace,
    }


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
    total_tokens = 0
    messages: list[dict] = [{"role": "user", "content": task}]
    trace: list[dict] = []

    for step in range(1, max_steps + 1):
        resp = client.chat(messages, tools=tools)
        total_tokens += resp.usage.total_tokens
        if token_budget is not None and total_tokens > token_budget:
            return _agent_result("budget", step, trace)
        if not resp.tool_calls:
            return _agent_result("final", step, trace, answer=resp.content or "")

        tc = resp.tool_calls[0]
        args = dict(tc.arguments)
        if trace and trace[-1]["tool"] == tc.name and trace[-1]["args"] == args:
            return _agent_result("repeat", step, trace)

        observation = _dispatch(tc, registry, required_map)
        assistant_msg = {
            "role": "assistant",
            "content": None,
            "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": args}],
        }
        messages.extend([
            assistant_msg,
            {"role": "tool", "tool_call_id": tc.id, "content": observation},
        ])
        trace.append({"step": step, "tool": tc.name, "args": args, "observation": observation})

    return _agent_result("max_steps", max_steps, trace)
