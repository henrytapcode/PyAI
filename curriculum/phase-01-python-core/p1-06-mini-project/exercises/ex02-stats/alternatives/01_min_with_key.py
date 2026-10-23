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


def best_key(row):
    """Smallest key wins: highest average first, then the earlier name."""
    return (-row["avg"], row["name"])


def worst_key(row):
    """Smallest key wins: lowest average first, then the earlier name."""
    return (row["avg"], row["name"])


def class_stats(students):
    """Same result as the loop version, using min(..., key=...) to find best and worst."""
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
        rows.append({"name": student["name"], "avg": avg})
        grade_counts[letter_grade(avg)] += 1

    total = sum(row["avg"] for row in rows)
    best = min(rows, key=best_key)
    worst = min(rows, key=worst_key)
    return {
        "count": len(rows),
        "mean": total / len(rows),
        "best": best["name"],
        "worst": worst["name"],
        "grade_counts": grade_counts,
    }
