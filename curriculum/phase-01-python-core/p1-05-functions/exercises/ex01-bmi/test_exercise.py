import pytest

from exercise import bmi, bmi_category


def test_bmi_of_80kg_and_2m_is_20():
    assert bmi(80, 2.0) == pytest.approx(20.0)


def test_bmi_with_decimal_height():
    assert bmi(52, 1.60) == pytest.approx(20.3125)


def test_bmi_returns_a_number_not_none():
    assert bmi(70, 1.75) is not None


def test_category_underweight():
    assert bmi_category(17.0) == "underweight"


def test_category_normal_includes_lower_limit():
    assert bmi_category(18.5) == "normal"
    assert bmi_category(22.0) == "normal"


@pytest.mark.parametrize("value, label", [
        (25.0, "overweight"),
        (29.9, "overweight"),
        (30.0, "obese"),
        (41.2, "obese"),
    ])
def test_category_upper_ranges(value, label):
    assert bmi_category(value) == label
