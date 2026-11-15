def build_messages(
    system: str,
    history: list[tuple[str, str]],
    user: str,
) -> list[dict[str, str]]:
    """Build a chat message list from a system prompt, past pairs, and a new user message.

    Example: build_messages("Be brief.", [("Hi", "Hello!")], "Bye") -> 4 message dicts
    """
    # TODO: replace each ___ blank with the right role name or content variable
    messages = [{"role": ___, "content": system}]
    for prev_user, prev_assistant in history:
        messages.append({"role": "user", "content": ___})
        messages.append({"role": ___, "content": prev_assistant})
    messages.append({"role": "user", "content": ___})
    return messages
