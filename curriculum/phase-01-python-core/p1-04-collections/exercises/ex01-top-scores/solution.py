def top_scores(scores, n):
    """Return the n biggest numbers in `scores`, biggest first."""
    ordered = sorted(scores, reverse=True)
    return ordered[:n]
