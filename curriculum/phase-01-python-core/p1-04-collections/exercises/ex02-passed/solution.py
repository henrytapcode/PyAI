def passed(scores, threshold):
    """Return a sorted list of names whose score is >= threshold."""
    result = []
    for name, score in scores.items():
        if score >= threshold:
            result.append(name)
    return sorted(result)
