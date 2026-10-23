def top_scores(scores, n):
    """Return the n biggest numbers in `scores`, biggest first."""
    copy = scores[:]
    copy.sort(reverse=True)
    return copy[:n]
