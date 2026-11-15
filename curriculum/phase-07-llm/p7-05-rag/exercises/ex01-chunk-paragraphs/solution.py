def chunk_paragraphs(text: str, max_words: int) -> list[str]:
    """Group non-empty paragraphs separated by '\\n\\n' up to max_words per chunk.

    Example: chunk_paragraphs("One two.\\n\\nThree.\\n\\nFour five six.", max_words=3)
    -> ["One two.\\n\\nThree.", "Four five six."]
    """
    if max_words <= 0:
        raise ValueError("max_words must be positive")
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_words = 0
    for para in paragraphs:
        word_count = len(para.split())
        if current and current_words + word_count > max_words:
            chunks.append("\n\n".join(current))
            current = [para]
            current_words = word_count
        else:
            current.append(para)
            current_words += word_count
    if current:
        chunks.append("\n\n".join(current))
    return chunks
