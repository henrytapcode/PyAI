import pytest

from exercise import report_line


def test_small_row_matches_example():
    assert report_line("small", 12345, 3.5) == "small           12,345    3.50"


def test_row_has_fixed_width():
    assert len(report_line("x", 1, 1.0)) == 30, "the row must be 12 + 10 + 8 = 30 characters"


def test_tokens_have_thousands_separators():
    line = report_line("gpt", 1250000, 0.5)
    assert "1,250,000" in line, "use the comma spec so 1250000 becomes 1,250,000"


def test_cost_is_rounded_to_two_decimals():
    assert report_line("big", 987, 0.126) == "big                987    0.13"


def test_returns_a_string_not_none():
    assert isinstance(report_line("a", 1, 1.0), str)


@pytest.mark.parametrize("model, tokens, cost, expected", [
    ("embed", 910, 0.0182, "embed              910    0.02"),
    ("gpt-large", 48200, 241.0, "gpt-large       48,200  241.00"),
])
def test_more_rows(model, tokens, cost, expected):
    assert report_line(model, tokens, cost) == expected
