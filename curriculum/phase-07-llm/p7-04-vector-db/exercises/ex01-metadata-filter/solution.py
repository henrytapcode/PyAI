def matches(metadata: dict, where: dict | None) -> bool:
    """Return True when metadata matches every key/value pair in where.

    Example: matches({"lang": "vi", "topic": "faq"}, {"lang": "vi"}) -> True
    """
    if not where:
        return True
    for key, value in where.items():
        if key not in metadata or metadata[key] != value:
            return False
    return True


def filter_indexes(metadatas: list[dict], where: dict | None) -> list[int]:
    """Return indexes (in original order) of metadata dicts matching where.

    Example: filter_indexes([{"lang": "en"}, {"lang": "vi"}], {"lang": "vi"}) -> [1]
    """
    kept: list[int] = []
    for idx, meta in enumerate(metadatas):
        if matches(meta, where):
            kept.append(idx)
    return kept
