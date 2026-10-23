"""Expense tracker, part 1: the model, the checks and the JSON file.

Write your code inside the class and the functions. Helper functions are welcome.
"""
import json
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from pathlib import Path


# TODO 1: make Expense a frozen dataclass with the fields
#         date (str), category (str), amount (float) and note (str, default "")
class Expense:
    pass


def check_expense(expense: Expense) -> None:
    """Raise ValueError if the expense breaks a rule, otherwise return None.

    Example: check_expense(Expense("2024-3-5", "food", 4.5)) raises ValueError (bad date)
    """
    # TODO 2: check the date, then the category, then the amount (see the rules in the prompt)
    pass


def save_expenses(path, expenses: list[Expense]) -> None:
    """Write the expenses to `path` as a JSON list of objects.

    Example: save_expenses("e.json", [Expense("2024-03-05", "food", 4.5, "pho")])
    """
    # TODO 3: check every expense first (so a bad one stops the save before any writing)
    # TODO 4: open the file for writing (utf-8) and dump the list of dicts
    pass


def load_expenses(path) -> list[Expense]:
    """Read the file at `path` and return a list of Expense objects.

    Example: load_expenses("e.json") -> [Expense(date='2024-03-05', category='food', ...)]
    """
    # TODO 5: read the JSON; if it is not a list, raise ValueError
    # TODO 6: turn each record into an Expense (a bad record becomes ValueError) and check it
    return None


@contextmanager
def edit_expenses(path):
    """Load the expenses of `path`, let the with-block change them, then save them.

    Example: with edit_expenses("e.json") as expenses:
                 expenses.append(Expense("2024-03-05", "food", 4.5))
    A missing file starts as []. If the block fails, nothing is saved.
    """
    # TODO 7: load the expenses if the file exists, otherwise start with an empty list
    # TODO 8: yield the list so the with-block can change it
    # TODO 9: after the block, save the list (this line is skipped when the block fails)
    yield []
