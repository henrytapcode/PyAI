def average(scores):
    """Return the mean of a list of numbers (0.0 for an empty list)."""
    return sum(scores) / len(scores) if scores else 0.0


def letter_grade(avg):
    """Return "A", "B", "C", "D" or "F" for an average on a 10-point scale."""
    for cutoff, grade in ((8.5, "A"), (7, "B"), (5.5, "C"), (4, "D")):
        if avg >= cutoff:
            return grade
    return "F"


def sort_key(row):
    """Highest average first; equal averages are ordered by name (A to Z)."""
    return (-row["avg"], row["name"])


def build_report(students):
    """Return a list of lines like "An: 8.17 (B)", best average first, ties by name."""
    rows = [{"name": s["name"], "avg": average(s["scores"])} for s in students]
    return [
        f"{row['name']}: {row['avg']:.2f} ({letter_grade(row['avg'])})"
        for row in sorted(rows, key=sort_key)
    ]
