import pytest

import exercise

CLASS = [
    {"name": "An", "scores": [8, 7.5, 9]},
    {"name": "Binh", "scores": [9, 9.5, 8.5]},
    {"name": "Chi", "scores": [5, 6, 4.5]},
]

EMPTY_COUNTS = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}


def test_result_has_the_five_keys():
    stats = exercise.class_stats(CLASS)
    assert sorted(stats.keys()) == ["best", "count", "grade_counts", "mean", "worst"]


def test_count_is_number_of_students():
    assert exercise.class_stats(CLASS)["count"] == 3, "count = number of students"


def test_mean_is_mean_of_student_averages():
    expected = (24.5 / 3 + 9 + 15.5 / 3) / 3
    assert exercise.class_stats(CLASS)["mean"] == pytest.approx(expected)


def test_best_and_worst_names():
    stats = exercise.class_stats(CLASS)
    assert stats["best"] == "Binh"
    assert stats["worst"] == "Chi"


def test_grade_counts_include_every_letter():
    stats = exercise.class_stats(CLASS)
    expected = {"A": 1, "B": 1, "C": 0, "D": 1, "F": 0}
    assert stats["grade_counts"] == expected, "start all five letters at 0, add 1 per student"


@pytest.mark.parametrize(
    "scores_list, expected",
    [
        ([[10], [9], [8.5]], {"A": 3, "B": 0, "C": 0, "D": 0, "F": 0}),
        ([[7], [6], [5], [3]], {"A": 0, "B": 1, "C": 1, "D": 1, "F": 1}),
        ([[1], [2], [3.9]], {"A": 0, "B": 0, "C": 0, "D": 0, "F": 3}),
    ],
)
def test_grade_counts_for_various_classes(scores_list, expected):
    students = [{"name": f"S{i}", "scores": s} for i, s in enumerate(scores_list)]
    assert exercise.class_stats(students)["grade_counts"] == expected


def test_ties_for_best_and_worst_go_to_first_name():
    students = [
        {"name": "Zoe", "scores": [9]},
        {"name": "Anh", "scores": [9]},
        {"name": "Mai", "scores": [3]},
        {"name": "Bao", "scores": [3]},
    ]
    stats = exercise.class_stats(students)
    assert stats["best"] == "Anh"
    assert stats["worst"] == "Bao"


def test_student_without_scores_counts_as_zero():
    students = [
        {"name": "An", "scores": [10]},
        {"name": "Ha", "scores": []},
    ]
    stats = exercise.class_stats(students)
    assert stats["mean"] == pytest.approx(5.0)
    assert stats["worst"] == "Ha"
    assert stats["grade_counts"] == {"A": 1, "B": 0, "C": 0, "D": 0, "F": 1}


def test_single_student_is_both_best_and_worst():
    stats = exercise.class_stats([{"name": "Lam", "scores": [6, 8]}])
    assert stats["count"] == 1
    assert stats["mean"] == pytest.approx(7.0)
    assert stats["best"] == "Lam"
    assert stats["worst"] == "Lam"


def test_empty_class():
    stats = exercise.class_stats([])
    assert stats["count"] == 0
    assert stats["mean"] == 0.0
    assert stats["best"] is None
    assert stats["worst"] is None
    assert stats["grade_counts"] == EMPTY_COUNTS
