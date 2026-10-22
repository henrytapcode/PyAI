import pytest

import exercise


@pytest.mark.parametrize("score", [100, 95, 90])
def test_a_for_90_and_above(score):
    assert exercise.grade(score) == "A"


@pytest.mark.parametrize("score", [89, 85, 80])
def test_b_for_80_to_89(score):
    assert exercise.grade(score) == "B"


@pytest.mark.parametrize("score", [79, 70])
def test_c_for_70_to_79(score):
    assert exercise.grade(score) == "C"


@pytest.mark.parametrize("score", [69, 60])
def test_d_for_60_to_69(score):
    assert exercise.grade(score) == "D"


@pytest.mark.parametrize("score", [59, 30, 0])
def test_f_below_60(score):
    assert exercise.grade(score) == "F"
