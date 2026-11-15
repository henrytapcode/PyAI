def build_messages(
    system: str,
    history: list[tuple[str, str]],
    user: str,
) -> list[dict[str, str]]:
    """Build a chat message list from a system prompt, past pairs, and a new user message.

    Example: build_messages("Be brief.", [("Hi", "Hello!")], "Bye") -> 4 message dicts
    """
    messages = [{"role": "system", "content": system}]
    for prev_user, prev_assistant in history:
        messages.append({"role": "user", "content": prev_user})
        messages.append({"role": "assistant", "content": prev_assistant})
    messages.append({"role": "user", "content": user})
    return messages
