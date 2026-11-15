def is_repeat(history: list[tuple[str, dict]], name: str, args: dict) -> bool:
    """Return True if (name, args) matches the immediately preceding step in history.

    Example:
        is_repeat([("lookup_order", {"order_id": "1042"})], "lookup_order", {"order_id": "1042"})
        -> True
    """
    # TODO: replace each ___ blank to check empty history and compare against the last entry
    if ___:
        return False
    last_name, last_args = ___
    return ___
