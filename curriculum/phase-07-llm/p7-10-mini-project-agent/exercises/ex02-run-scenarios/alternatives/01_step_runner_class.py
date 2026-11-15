class _AgentSession:
    """Encapsulates one scenario execution state machine step by step."""

    def __init__(self, client, toolbox, scenario: dict) -> None:
        self.client = client
        self.toolbox = toolbox
        self.token_budget = scenario.get("token_budget")
        self.approve = scenario.get("approve")
        self.messages = [{"role": "user", "content": scenario["task"]}]
        self.tools_run: list[str] = []
        self.last_call: tuple[str, dict] | None = None
        self.tokens = 0
        self.answer = ""

    def step(self) -> str | None:
        resp = self.client.chat(self.messages, tools=self.toolbox.schemas())
        self.tokens += resp.usage.total_tokens
        if self.token_budget is not None and self.tokens > self.token_budget:
            return "budget"
        if not resp.tool_calls:
            self.answer = resp.content or ""
            return "final"
        tc = resp.tool_calls[0]
        args = dict(tc.arguments)
        if self.last_call == (tc.name, args):
            return "repeat"
        if self.toolbox.is_side_effect(tc.name):
            if self.approve is None or not self.approve(tc.name, dict(args)):
                return "needs_approval"
        obs = self.toolbox.call(tc.name, dict(args))
        self.messages.append(
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": args}],
            }
        )
        self.messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
        self.last_call = (tc.name, args)
        self.tools_run.append(tc.name)
        return None


def run_scenario(scenario: dict, toolbox, make_client) -> dict:
    """Run one scenario using _AgentSession.step() and score expectations."""
    session = _AgentSession(make_client(list(scenario["script"])), toolbox, scenario)
    stopped_reason = "max_steps"
    for _ in range(scenario.get("max_steps", 6)):
        verdict = session.step()
        if verdict is not None:
            stopped_reason = verdict
            break

    expect = scenario["expect"]
    checks = [
        ("stopped_reason", stopped_reason != expect["stopped_reason"]),
        ("tools", session.tools_run != expect["tools"]),
        (
            "answer",
            bool(expect.get("answer_contains"))
            and expect["answer_contains"].lower() not in session.answer.lower(),
        ),
    ]
    reasons = [label for label, failed in checks if failed]
    return {
        "name": scenario["name"],
        "passed": not reasons,
        "stopped_reason": stopped_reason,
        "tools": session.tools_run,
        "reasons": reasons,
    }


def summarize(results: list[dict]) -> list[str]:
    """Format pass count, FAIL rows, or final all-passed marker."""
    ok_total = sum(1 for r in results if r["passed"])
    fail_rows = [f"FAIL {r['name']}: {', '.join(r['reasons'])}" for r in results if not r["passed"]]
    tail = fail_rows if fail_rows else ["all passed"]
    return [f"passed: {ok_total}/{len(results)}", *tail]
