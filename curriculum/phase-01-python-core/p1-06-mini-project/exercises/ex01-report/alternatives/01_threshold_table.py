def average(scores):
    """Return the mean of a list of numbers, or 0.0 for an empty list."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


# (minimum average, letter), checked from the top down
GRADE_TABLE = [(8.5, "A"), (7, "B"), (5.5, "C"), (4, "D")]


def letter_grade(avg):
    """Return the letter by looping over a lookup table instead of an if chain."""
    for minimum, letter in GRADE_TABLE:
        if avg >= minimum:
            return letter
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
        lines.append(f"{row['name']}: {row['avg']:.2f} ({letter_grade(row['avg'])})")
    return lines
