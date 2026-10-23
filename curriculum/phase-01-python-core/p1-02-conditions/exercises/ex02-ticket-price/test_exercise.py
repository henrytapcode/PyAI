import pytest

import exercise


@pytest.mark.parametrize("age", [0, 4])
def test_free_under_five(age):
    assert exercise.ticket_price(age, False) == 0


def test_five_year_old_is_not_free():
    assert exercise.ticket_price(5, False) == 6


@pytest.mark.parametrize("age", [8, 11, 65, 80])
def test_children_and_seniors_pay_six(age):
    assert exercise.ticket_price(age, False) == 6


def test_twelve_year_old_pays_full_price():
    assert exercise.ticket_price(12, False) == 12


@pytest.mark.parametrize("age", [18, 25])
def test_young_students_pay_nine(age):
    assert exercise.ticket_price(age, True) == 9


def test_old_student_pays_full_price():
    assert exercise.ticket_price(30, True) == 12


def test_adult_non_student_pays_full_price():
    assert exercise.ticket_price(40, False) == 12


def test_student_just_over_twenty_five_pays_full_price():
    assert exercise.ticket_price(26, True) == 12


def test_adult_just_under_senior_age_pays_full_price():
    assert exercise.ticket_price(64, False) == 12


def test_child_student_pays_six():
    assert exercise.ticket_price(10, True) == 6
