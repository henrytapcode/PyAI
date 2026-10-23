def passed(scores, threshold):
    """Return a sorted list of names whose score is >= threshold."""
    result = []
    for name in scores:
        if scores[name] >= threshold:
            result.append(name)
    return sorted(result)
