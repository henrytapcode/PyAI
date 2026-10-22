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

    best_name = students[0]["name"]
    best_avg = average(students[0]["scores"])
    worst_name = best_name
    worst_avg = best_avg
    total = 0

    for student in students:
        name = student["name"]
        avg = average(student["scores"])
        total += avg
        grade_counts[letter_grade(avg)] += 1

        # ties go to the name that comes first alphabetically
        if avg > best_avg or (avg == best_avg and name < best_name):
            best_name = name
            best_avg = avg
        if avg < worst_avg or (avg == worst_avg and name < worst_name):
            worst_name = name
            worst_avg = avg

    return {
        "count": len(students),
        "mean": total / len(students),
        "best": best_name,
        "worst": worst_name,
        "grade_counts": grade_counts,
    }
