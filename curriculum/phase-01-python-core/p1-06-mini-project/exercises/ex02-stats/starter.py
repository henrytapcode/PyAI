"""Grade report, part 2: statistics for the whole class.

`average` and `letter_grade` are finished for you (you wrote them in exercise 1).
Complete `class_stats`: write your code inside the function and `return` the answer.
"""


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
    """Return {"count", "mean", "best", "worst", "grade_counts"} for the class.

    Example: class_stats([{"name": "An", "scores": [8, 7.5, 9]},
                          {"name": "Binh", "scores": [9, 9.5, 8.5]}])
    -> {"count": 2, "mean": 8.583..., "best": "Binh", "worst": "An",
        "grade_counts": {"A": 1, "B": 1, "C": 0, "D": 0, "F": 0}}
    """
    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    # TODO 1: empty class -> return count 0, mean 0.0, best None, worst None and grade_counts

    # TODO 2: start best_name/best_avg (and worst_name/worst_avg) from the first student

    # TODO 3: loop over the students. For each one:
    #   - compute its average
    #   - add it to a running total
    #   - add 1 to grade_counts[its letter]
    #   - replace best if the average is higher (or equal with an earlier name)
    #   - replace worst if the average is lower (or equal with an earlier name)

    # TODO 4: return the dict (mean = total / number of students)
    return None
