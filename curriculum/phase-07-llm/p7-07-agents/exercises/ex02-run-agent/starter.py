import json


def run_agent(
    client,
    task: str,
    tools: list[dict],
    registry: dict,
    max_steps: int = 5,
    token_budget: int | None = None,
) -> dict:
    """Run a bounded observe-think-act agent loop with trace and stop conditions.

    Example:
        run_agent(FakeLLM(script=script), "When will order 1042 arrive?", tools, registry)
        -> {"answer": "...", "stopped_reason": "final", "steps": 3, "trace": [...]}
    """
    # TODO: initialize messages, trace, total_tokens, and required_map
    # TODO: loop step from 1 to max_steps calling client.chat(messages, tools=tools)
    # TODO: check stop conditions in order: budget -> final -> repeat
    # TODO: dispatch first tool call safely, append assistant + tool messages, record trace
    # TODO: return stopped_reason="max_steps" if the loop exhausts max_steps
    _ = json
    return None
