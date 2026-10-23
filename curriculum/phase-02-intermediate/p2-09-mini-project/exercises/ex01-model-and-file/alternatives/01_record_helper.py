"""Expense tracker, part 1, with a small helper that turns one record into an Expense."""
import json
from contextlib import contextmanager
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Expense:
    date: str
    category: str
    amount: float
    note: str = ""


def check_expense(expense: Expense) -> None:
    parts = expense.date.split("-") if isinstance(expense.date, str) else []
    sizes = [len(part) for part in parts]
    if sizes != [4, 2, 2] or not "".join(parts).isdigit():
        raise ValueError(f"date must look like YYYY-MM-DD, got {expense.date!r}")
    if not isinstance(expense.category, str) or expense.category.strip() == "":
        raise ValueError("category must not be empty")
    if not isinstance(expense.amount, (int, float)) or expense.amount <= 0:
        raise ValueError(f"amount must be a number above 0, got {expense.amount!r}")


def record_to_expense(record) -> Expense:
    try:
        expense = Expense(**record)
    except TypeError as err:
        raise ValueError(f"bad record {record!r}: {err}") from None
    check_expense(expense)
    return expense


def save_expenses(path, expenses: list[Expense]) -> None:
    for expense in expenses:
        check_expense(expense)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(expense) for expense in expenses], f)


def load_expenses(path) -> list[Expense]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("the file must hold a list of expenses")
    return [record_to_expense(record) for record in data]


@contextmanager
def edit_expenses(path):
    try:
        expenses = load_expenses(path)
    except FileNotFoundError:
        expenses = []
    yield expenses
    save_expenses(path, expenses)
