def top_scores(scores, n):
    """Return the n biggest numbers in `scores`, biggest first."""
    ordered = sorted(scores, reverse=True)
    top = []
    for score in ordered:
        if len(top) == n:
            break
        top.append(score)
    return top
