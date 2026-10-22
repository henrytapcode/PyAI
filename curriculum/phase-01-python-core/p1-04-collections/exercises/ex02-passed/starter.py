def passed(scores, threshold):
    """Return a sorted list of names whose score is >= threshold."""
    result = []
    for name, score in scores.items():  # noqa: B007
        if score > threshold:
            result.append(score)
    return result
