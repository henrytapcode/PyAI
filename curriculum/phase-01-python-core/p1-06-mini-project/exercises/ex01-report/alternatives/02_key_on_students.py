def average(scores):
    """Return the mean of a list of numbers, or 0.0 for an empty list."""
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


def student_key(student):
    """Same idea as sort_key, but it works directly on a student dict."""
    return (-average(student["scores"]), student["name"])


def build_report(students):
    """Sort the students themselves, then build each line."""
    lines = []
    for student in sorted(students, key=student_key):
        avg = average(student["scores"])
        lines.append(f"{student['name']}: {avg:.2f} ({letter_grade(avg)})")
    return lines
