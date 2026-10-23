def word_count(words):
    """Return a dict mapping each word in `words` to how many times it appears."""
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts
