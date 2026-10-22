def average(scores):
    """Mean of a list of numbers (0.0 for an empty list). Already done for you."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def letter_grade(avg):
    """Letter for an average on a 10-point scale. Already done for you."""
    if avg >= 8.5:
        return "A"
    if avg >= 7:
        return "B"
    if avg >= 5.5:
        return "C"
    if avg >= 4:
        return "D"
    return "F"


def class_stats(students):
    """Return {"count", "mean", "best", "worst", "grade_counts"} for the class."""
    pass
