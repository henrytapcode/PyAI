"""Expense tracker, part 2: the report.

`Expense` is finished for you (you wrote it in exercise 1).
Complete the three report functions: write your code inside them and `return` the answer.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Expense:
    date: str
    category: str
    amount: float
    note: str = ""


def totals_by_category(expenses: list[Expense]) -> dict[str, float]:
    """Total amount per category, with sorted keys and totals rounded to 2 decimals.

    Example: [Expense("2024-01-05", "food", 4.5), Expense("2024-01-09", "fun", 9.0),
              Expense("2024-02-01", "food", 6.25)]
    -> {"food": 10.75, "fun": 9.0}
    """
    # TODO 1: start with an empty dict
    # TODO 2: loop over the expenses and add each amount to its category
    # TODO 3: return a new dict with the keys in sorted order and each total rounded
    return None


def totals_by_month(expenses: list[Expense]) -> dict[str, float]:
    """Total amount per month ("YYYY-MM"), oldest month first, totals rounded to 2 decimals.

    Example: the same three expenses -> {"2024-01": 13.5, "2024-02": 6.25}
    """
    # TODO 4: same idea as above, but the key is the first 7 characters of the date
    return None


def top_category(expenses: list[Expense]) -> str | None:
    """Name of the category with the biggest total, or None for an empty list.

    Example: the same three expenses -> "food"
    """
    # TODO 5: use totals_by_category and the "best so far" loop
    return None
