import json


class Agent:
    """Stateful single-agent runner exposing step() and run()."""

    def __init__(
        self,
        client,
        tools: list[dict],
        registry: dict,
        max_steps: int = 5,
        token_budget: int | None = None,
    ) -> None:
        self.client = client
        self.tools = list(tools)
        self.registry = dict(registry)
        self.max_steps = max_steps
        self.token_budget = token_budget
        self.required_map = {
            t["name"]: set(t.get("parameters", {}).get("required", []))
            for t in self.tools
        }
        self.messages: list[dict] = []
        self.trace: list[dict] = []
        self.total_tokens = 0
        self.steps = 0

    def _dispatch(self, tc) -> str:
        fn = self.registry.get(tc.name)
        if fn is None:
            return f"error: unknown tool {tc.name}"
        req = self.required_map.get(tc.name, set())
        clean = {k: v for k, v in tc.arguments.items() if k in req or v not in ("", None)}
        try:
            out = fn(**clean)
        except Exception as err:
            return f"error: {err}"
        return json.dumps(out) if isinstance(out, dict) else str(out)

    def _result(self, answer: str, stopped_reason: str, steps: int) -> dict:
        return {
            "answer": answer,
            "stopped_reason": stopped_reason,
            "steps": steps,
            "trace": self.trace,
        }

    def step(self) -> dict | None:
        """Execute one observe-think-act cycle; return final dict if stopped, else None."""
        self.steps += 1
        resp = self.client.chat(self.messages, tools=self.tools)
        self.total_tokens += resp.usage.total_tokens
        if self.token_budget is not None and self.total_tokens > self.token_budget:
            return self._result("", "budget", self.steps)
        if not resp.tool_calls:
            return self._result(resp.content or "", "final", self.steps)

        tc = resp.tool_calls[0]
        args = dict(tc.arguments)
        if self.trace and self.trace[-1]["tool"] == tc.name and self.trace[-1]["args"] == args:
            return self._result("", "repeat", self.steps)

        observation = self._dispatch(tc)
        self.messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [{"id": tc.id, "name": tc.name, "arguments": args}],
        })
        self.messages.append({"role": "tool", "tool_call_id": tc.id, "content": observation})
        self.trace.append({
            "step": self.steps,
            "tool": tc.name,
            "args": args,
            "observation": observation,
        })
        return None

    def run(self, task: str) -> dict:
        """Run up to max_steps cycles for task and return the final result dict."""
        self.messages = [{"role": "user", "content": task}]
        self.trace = []
        self.total_tokens = 0
        self.steps = 0
        for _ in range(self.max_steps):
            done = self.step()
            if done is not None:
                return done
        return self._result("", "max_steps", self.max_steps)


def run_agent(
    client,
    task: str,
    tools: list[dict],
    registry: dict,
    max_steps: int = 5,
    token_budget: int | None = None,
) -> dict:
    """Delegate to the Agent class."""
    return Agent(
        client,
        tools,
        registry,
        max_steps=max_steps,
        token_budget=token_budget,
    ).run(task)
