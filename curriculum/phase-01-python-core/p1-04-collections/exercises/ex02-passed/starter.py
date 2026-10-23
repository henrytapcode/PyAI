def passed(scores, threshold):
    """Return a sorted list of the names whose score is >= threshold.

    Example: passed({"Minh": 8, "Lan": 5, "Hoa": 3}, 5) returns ["Lan", "Minh"]
    """
    # This code runs, but it has 3 bugs. Press Check and read the failing tests.
    result = []
    for name, score in scores.items():
        if score > threshold:
            result.append((name, score))
    return result
