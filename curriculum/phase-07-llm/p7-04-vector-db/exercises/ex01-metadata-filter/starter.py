def matches(metadata: dict, where: dict | None) -> bool:
    """Return True when metadata matches every key/value pair in where.

    Example: matches({"lang": "vi", "topic": "faq"}, {"lang": "vi"}) -> True
    """
    # TODO: replace each ___ blank to handle empty filters and check every key/value
    if ___:
        return True
    for key, value in where.items():
        if ___:
            return False
    return True


def filter_indexes(metadatas: list[dict], where: dict | None) -> list[int]:
    """Return indexes (in original order) of metadata dicts matching where.

    Example: filter_indexes([{"lang": "en"}, {"lang": "vi"}], {"lang": "vi"}) -> [1]
    """
    # TODO: replace ___ to keep matching indexes in order
    kept: list[int] = []
    for idx, meta in enumerate(metadatas):
        if ___:
            kept.append(idx)
    return kept
