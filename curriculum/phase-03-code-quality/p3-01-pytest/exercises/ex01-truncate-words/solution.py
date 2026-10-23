def truncate_words(text: str, limit: int) -> str:
    """Keep at most `limit` words of `text`.

    Example:
        truncate_words("one two three four", 2) -> "one two..."
    """
    if limit < 0:
        raise ValueError("limit must be 0 or more")
    words = text.split()
    if len(words) <= limit:
        return " ".join(words)
    return " ".join(words[:limit]) + "..."
