import pytest

from exercise import age_or_none, validate_age


def test_valid_age_is_returned():
    assert validate_age(30) == 30


@pytest.mark.parametrize("age", [0, 120])
def test_limits_are_valid(age):
    assert validate_age(age) == age


@pytest.mark.parametrize("age", [-1, 121, 200])
def test_out_of_range_raises_value_error(age):
    with pytest.raises(ValueError):
        validate_age(age)


def test_error_message_contains_the_bad_value():
    with pytest.raises(ValueError, match="age must be between 0 and 120, got 200"):
        validate_age(200)


def test_age_or_none_returns_age_for_good_text():
    assert age_or_none("25") == 25


@pytest.mark.parametrize("text", ["x", "", "twenty", "200", "-5"])
def test_age_or_none_returns_none_for_bad_text(text):
    assert age_or_none(text) is None
