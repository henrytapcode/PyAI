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


def build_report(students):
    """Return a list of lines like "An: 8.17 (B)", best average first, ties by name."""
    rows = []
    for student in students:
        rows.append((student["name"], average(student["scores"])))
    rows.sort(key=lambda row: (-row[1], row[0]))
    return [f"{name}: {avg:.2f} ({letter_grade(avg)})" for name, avg in rows]
