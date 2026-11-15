def chunk_words(text: str, size: int, overlap: int) -> list[str]:
    """Split text into overlapping word windows joined by single spaces.

    Example: chunk_words("a b c d e", size=3, overlap=1) -> ["a b c", "c d e"]
    """
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("need size > 0 and 0 <= overlap < size")
    words = text.split()
    if not words:
        return []
    step = size - overlap
    chunks: list[str] = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i : i + size]))
        if i + size >= len(words):
            break
        i += step
    return chunks
