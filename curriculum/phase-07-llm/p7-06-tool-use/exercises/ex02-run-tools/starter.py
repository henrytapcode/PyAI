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
    # TODO: start messages with the user question and track called tool names
    # TODO: loop up to max_rounds calling client.chat(messages, tools=tools)
    # TODO: if no tool_calls, return (resp.content or "", called)
    # TODO: append assistant tool_calls message, dispatch each call safely, append tool messages
    # TODO: return ("stopped: too many tool calls", called) if max_rounds is exhausted
    _ = json
    return None
