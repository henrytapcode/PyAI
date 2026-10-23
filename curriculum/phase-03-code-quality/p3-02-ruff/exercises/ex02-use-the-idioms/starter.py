def describe(data):
    """Say how many rows `data` has, or "no data" when it is None.

    Example:
        describe(None) -> "no data"
        describe([1, 2]) -> "got 2 rows"
    """
    # Replace each ___ with the idiom ruff asks for (see §7).
    if ___:
        return "no data"
    return f"got {len(data)} rows"


def is_unknown(label, known):
    """Return True when `label` is not in the collection `known`.

    Example:
        is_unknown("eggs", {"spam", "ham"}) -> True
    """
    return ___


def switch_state(flag):
    """Return "on" when `flag` is truthy (True, a non-empty text, a non-zero number), else "off".

    Example:
        switch_state("yes") -> "on"
        switch_state(0) -> "off"
    """
    if ___:
        return "on"
    return "off"
