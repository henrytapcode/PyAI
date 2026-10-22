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
    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    if not students:
        return {
            "count": 0,
            "mean": 0.0,
            "best": None,
            "worst": None,
            "grade_counts": grade_counts,
        }

    rows = []
    for student in students:
        avg = average(student["scores"])
        rows.append((student["name"], avg))
        grade_counts[letter_grade(avg)] += 1

    best = min(rows, key=lambda row: (-row[1], row[0]))[0]
    worst = min(rows, key=lambda row: (row[1], row[0]))[0]
    return {
        "count": len(rows),
        "mean": sum(avg for _, avg in rows) / len(rows),
        "best": best,
        "worst": worst,
        "grade_counts": grade_counts,
    }
