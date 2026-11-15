def is_repeat(history: list[tuple[str, dict]], name: str, args: dict) -> bool:
    """Return True if (name, args) matches the immediately preceding step in history.

    Example:
        is_repeat([("lookup_order", {"order_id": "1042"})], "lookup_order", {"order_id": "1042"})
        -> True
    """
    if not history:
        return False
    last_name, last_args = history[-1]
    return last_name == name and last_args == args
