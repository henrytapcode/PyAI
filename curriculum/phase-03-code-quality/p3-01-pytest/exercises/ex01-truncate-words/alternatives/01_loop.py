def truncate_words(text: str, limit: int) -> str:
    if limit < 0:
        raise ValueError("limit must be 0 or more")
    kept = []
    for word in text.split():
        if len(kept) == limit:
            return " ".join(kept) + "..."
        kept.append(word)
    return " ".join(kept)
