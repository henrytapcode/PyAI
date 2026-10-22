def grade(score):
    """Return "A", "B", "C", "D" or "F" for a score from 0 to 100."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
