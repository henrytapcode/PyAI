import pytest

from exercise import Expense, top_category, totals_by_category, totals_by_month

SAMPLE = [
    Expense("2024-01-05", "food", 4.5, "pho"),
    Expense("2024-01-12", "transport", 12.0),
    Expense("2024-01-20", "food", 6.25),
    Expense("2024-02-02", "fun", 9.0),
    Expense("2024-02-14", "food", 13.0),
    Expense("2024-02-20", "transport", 3.5),
]


def test_totals_by_category_adds_up_each_category():
    assert totals_by_category(SAMPLE) == {"food": 23.75, "fun": 9.0, "transport": 15.5}


def test_totals_by_category_keys_are_sorted():
    assert list(totals_by_category(SAMPLE)) == ["food", "fun", "transport"]
    reversed_input = list(reversed(SAMPLE))
    assert list(totals_by_category(reversed_input)) == ["food", "fun", "transport"]


def test_totals_are_rounded_to_two_decimals():
    expenses = [Expense("2024-01-01", "food", 0.1), Expense("2024-01-02", "food", 0.2)]
    assert totals_by_category(expenses) == {"food": 0.3}
    assert totals_by_month(expenses) == {"2024-01": 0.3}


def test_empty_list_gives_empty_totals():
    assert totals_by_category([]) == {}
    assert totals_by_month([]) == {}


def test_totals_by_month_adds_up_each_month():
    assert totals_by_month(SAMPLE) == {"2024-01": 22.75, "2024-02": 25.5}


def test_months_are_oldest_first_and_years_are_kept_apart():
    expenses = [
        Expense("2024-01-10", "food", 2.0),
        Expense("2023-12-30", "food", 3.0),
        Expense("2023-01-05", "food", 4.0),
    ]
    result = totals_by_month(expenses)
    assert list(result) == ["2023-01", "2023-12", "2024-01"]
    assert result["2023-01"] == 4.0


def test_the_input_list_is_not_changed():
    expenses = [SAMPLE[3], SAMPLE[0], SAMPLE[5], SAMPLE[1], SAMPLE[4], SAMPLE[2]]   # not sorted
    before = list(expenses)
    totals_by_category(expenses)
    totals_by_month(expenses)
    top_category(expenses)
    assert expenses == before, "do not sort or change the list you receive"


def test_top_category_is_the_biggest_total():
    assert top_category(SAMPLE) == "food"


def test_top_category_counts_the_sum_not_the_biggest_single_item():
    expenses = [
        Expense("2024-01-01", "travel", 20.0),
        Expense("2024-01-02", "food", 8.0),
        Expense("2024-01-03", "food", 8.0),
        Expense("2024-01-04", "food", 8.0),
    ]
    assert top_category(expenses) == "food", "add up the amounts of each category first"


def test_top_category_tie_goes_to_the_earlier_name():
    expenses = [
        Expense("2024-01-01", "zoo", 5.0),
        Expense("2024-01-02", "art", 2.5),
        Expense("2024-01-03", "art", 2.5),
        Expense("2024-01-04", "mid", 1.0),
    ]
    assert top_category(expenses) == "art"


def test_top_category_of_an_empty_list_is_none():
    assert top_category([]) is None


@pytest.mark.parametrize("name", ["food", "fun"])
def test_top_category_with_one_category(name):
    assert top_category([Expense("2024-01-01", name, 1.0)]) == name
