def _score_expectation(
    stopped_reason: str,
    tools_run: list[str],
    answer: str,
    expect: dict,
) -> list[str]:
    failures: list[str] = []
    if stopped_reason != expect["stopped_reason"]:
        failures.append("stopped_reason")
    if tools_run != expect["tools"]:
        failures.append("tools")
    target = expect.get("answer_contains")
    if target and target.lower() not in answer.lower():
        failures.append("answer")
    return failures


def run_scenario(scenario: dict, toolbox, make_client) -> dict:
    """Execute one scripted agent scenario with safety guards and compare to expect."""
    client = make_client(list(scenario["script"]))
    max_steps = scenario.get("max_steps", 6)
    token_budget = scenario.get("token_budget")
    approve_fn = scenario.get("approve")

    history = [{"role": "user", "content": scenario["task"]}]
    executed: list[tuple[str, dict]] = []
    tools_run: list[str] = []
    token_total = 0
    stopped_reason = "max_steps"
    final_answer = ""

    for _ in range(1, max_steps + 1):
        reply = client.chat(history, tools=toolbox.schemas())
        token_total += reply.usage.total_tokens
        if token_budget is not None and token_total > token_budget:
            stopped_reason = "budget"
            break
        if not reply.tool_calls:
            final_answer = reply.content or ""
            stopped_reason = "final"
            break
        tc = reply.tool_calls[0]
        call_args = dict(tc.arguments)
        if executed and executed[-1] == (tc.name, call_args):
            stopped_reason = "repeat"
            break
        if toolbox.is_side_effect(tc.name):
            if approve_fn is None:
                stopped_reason = "needs_approval"
                break
            if not approve_fn(tc.name, dict(call_args)):
                stopped_reason = "rejected"
                break
        observation = toolbox.call(tc.name, dict(call_args))
        history.append(
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": call_args}],
            }
        )
        history.append({"role": "tool", "tool_call_id": tc.id, "content": observation})
        executed.append((tc.name, call_args))
        tools_run.append(tc.name)

    reasons = _score_expectation(stopped_reason, tools_run, final_answer, scenario["expect"])
    return {
        "name": scenario["name"],
        "passed": len(reasons) == 0,
        "stopped_reason": stopped_reason,
        "tools": tools_run,
        "reasons": reasons,
    }


def summarize(results: list[dict]) -> list[str]:
    """Format scenario pass counts, per-failure reasons, and all-passed status."""
    passed_count = sum(1 for item in results if item["passed"])
    lines = [f"passed: {passed_count}/{len(results)}"]
    failed_items = [item for item in results if not item["passed"]]
    if not failed_items:
        lines.append("all passed")
        return lines
    for item in failed_items:
        lines.append(f"FAIL {item['name']}: {', '.join(item['reasons'])}")
    return lines
