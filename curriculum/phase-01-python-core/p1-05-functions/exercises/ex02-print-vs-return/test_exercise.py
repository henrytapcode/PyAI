import pytest

from exercise import area, greet, price_with_tax


def test_area_returns_the_value():
    assert area(3, 4) == 12


def test_area_result_can_be_used_in_maths():
    assert area(3, 4) + 1 == 13


def test_price_with_tax_uses_default_rate():
    assert price_with_tax(100) == pytest.approx(110.0)


def test_price_with_tax_accepts_custom_rate():
    assert price_with_tax(200, rate=0.5) == pytest.approx(300.0)


def test_greet_prints_default_and_custom_greeting(capsys):
    greet("Lan")
    assert capsys.readouterr().out == "Hello, Lan!\n"
    greet("Lan", greeting="Hi")
    assert capsys.readouterr().out == "Hi, Lan!\n"
