"""Grade report, part 1: average, letter grade, ranked report.

Four small functions, built from the bottom up. Write your code inside each
function and `return` the answer. Press Check often: one green test at a time.
"""


def average(scores):
    """Return the mean of a list of numbers, or 0.0 for an empty list.

    Example: average([8, 7.5, 9]) -> 8.1666...   average([]) -> 0.0
    """
    # TODO 1: if the list is empty, return 0.0
    # TODO 2: otherwise add the scores up (sum) and divide by how many there are (len)
    return None


def letter_grade(avg):
    """Return "A", "B", "C", "D" or "F" for an average on a 10-point scale.

    Example: letter_grade(8.5) -> "A"   letter_grade(7.2) -> "B"   letter_grade(3.9) -> "F"
    Scale: A >= 8.5, B >= 7, C >= 5.5, D >= 4, otherwise F.
    """
    # TODO: check from the highest threshold down, one `if ...: return "..."` each
    return None


def sort_key(row):
    """Sorting key for a row: highest average first, equal averages by name (A to Z).

    Example: sort_key({"name": "An", "avg": 8.5}) -> (-8.5, "An")
    """
    # TODO: return a tuple: the average with its sign flipped, then the name
    return None


def build_report(students):
    """Return a list of lines like "An: 8.17 (B)", best average first, ties by name.

    Example: build_report([{"name": "An", "scores": [8, 7.5, 9]}]) -> ["An: 8.17 (B)"]
    An empty class gives [].
    """
    # TODO 1: make a list `rows` with one dict {"name": ..., "avg": ...} per student
    # TODO 2: loop over sorted(rows, key=sort_key) and build one f-string per row
    #         (average with 2 decimals, then the letter grade in parentheses)
    # TODO 3: return the list of lines (do not print them)
    return None
