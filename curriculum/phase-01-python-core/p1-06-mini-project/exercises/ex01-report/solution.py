def average(scores):
    """Return the mean of a list of numbers (0.0 for an empty list)."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def letter_grade(avg):
    """Return "A", "B", "C", "D" or "F" for an average on a 10-point scale."""
    if avg >= 8.5:
        return "A"
    if avg >= 7:
        return "B"
    if avg >= 5.5:
        return "C"
    if avg >= 4:
        return "D"
    return "F"


def sort_key(row):
    """Highest average first; equal averages are ordered by name (A to Z)."""
    return (-row["avg"], row["name"])


def build_report(students):
    """Return a list of lines like "An: 8.17 (B)", best average first, ties by name."""
    rows = []
    for student in students:
        rows.append({"name": student["name"], "avg": average(student["scores"])})

    lines = []
    for row in sorted(rows, key=sort_key):
        avg = row["avg"]
        lines.append(f"{row['name']}: {avg:.2f} ({letter_grade(avg)})")
    return lines
