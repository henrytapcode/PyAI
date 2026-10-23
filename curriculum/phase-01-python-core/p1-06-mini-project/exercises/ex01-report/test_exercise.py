import pytest

import exercise


@pytest.mark.parametrize(
    "scores, expected",
    [
        ([8, 7.5, 9], 24.5 / 3),
        ([10], 10.0),
        ([5, 6], 5.5),
        ([0, 0, 0], 0.0),
    ],
)
def test_average_of_scores(scores, expected):
    assert exercise.average(scores) == pytest.approx(expected), "average = sum / len"


def test_average_returns_zero_for_empty_list():
    assert exercise.average([]) == 0.0, "an empty list must return 0.0, not crash"


@pytest.mark.parametrize(
    "avg, expected",
    [
        (10, "A"),
        (8.5, "A"),
        (8.49, "B"),
        (7, "B"),
        (6.99, "C"),
        (5.5, "C"),
        (5.49, "D"),
        (4, "D"),
        (3.99, "F"),
        (0, "F"),
    ],
)
def test_letter_grade_boundaries(avg, expected):
    assert exercise.letter_grade(avg) == expected, "use >= and go from the top down"


def test_report_has_one_line_per_student():
    students = [
        {"name": "An", "scores": [8, 7.5, 9]},
        {"name": "Binh", "scores": [9, 9.5, 8.5]},
        {"name": "Chi", "scores": [5, 6, 4.5]},
    ]
    assert len(exercise.build_report(students)) == 3, "return a list with one line per student"


def test_report_line_format():
    report = exercise.build_report([{"name": "An", "scores": [8, 7.5, 9]}])
    assert report == ["An: 8.17 (B)"]


def test_report_sorted_by_average_descending():
    students = [
        {"name": "An", "scores": [8, 7.5, 9]},
        {"name": "Binh", "scores": [9, 9.5, 8.5]},
        {"name": "Chi", "scores": [5, 6, 4.5]},
    ]
    assert exercise.build_report(students) == [
        "Binh: 9.00 (A)",
        "An: 8.17 (B)",
        "Chi: 5.17 (D)",
    ]


def test_report_breaks_ties_by_name():
    students = [
        {"name": "Zoe", "scores": [7, 7]},
        {"name": "Anh", "scores": [6, 8]},
        {"name": "Mai", "scores": [7]},
    ]
    assert exercise.build_report(students) == [
        "Anh: 7.00 (B)",
        "Mai: 7.00 (B)",
        "Zoe: 7.00 (B)",
    ]


def test_report_shows_two_decimals():
    report = exercise.build_report([{"name": "Lam", "scores": [8, 8, 9]}])
    assert report == ["Lam: 8.33 (B)"]


def test_report_student_without_scores_gets_f():
    report = exercise.build_report([{"name": "Ha", "scores": []}])
    assert report == ["Ha: 0.00 (F)"]


def test_report_for_empty_class_is_empty_list():
    assert exercise.build_report([]) == []


def test_sort_key_flips_average_and_keeps_name():
    assert exercise.sort_key({"name": "An", "avg": 8.5}) == (-8.5, "An")
