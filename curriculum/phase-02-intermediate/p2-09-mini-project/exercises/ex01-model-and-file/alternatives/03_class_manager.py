"""Expense tracker, part 1, with edit_expenses written as a class with __enter__ and __exit__."""
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Expense:
    date: str
    category: str
    amount: float
    note: str = ""


def looks_like_date(text: str) -> bool:
    parts = text.split("-")
    return [len(part) for part in parts] == [4, 2, 2] and "".join(parts).isdigit()


def check_expense(expense: Expense) -> None:
    if not isinstance(expense.date, str) or not looks_like_date(expense.date):
        raise ValueError(f"date must look like YYYY-MM-DD, got {expense.date!r}")
    if not isinstance(expense.category, str) or not expense.category.strip():
        raise ValueError("category must not be empty")
    if not isinstance(expense.amount, (int, float)) or expense.amount <= 0:
        raise ValueError(f"amount must be a number above 0, got {expense.amount!r}")


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
    expenses = []
    for record in data:
        try:
            expense = Expense(**record)
        except TypeError:
            raise ValueError(f"bad record: {record!r}") from None
        check_expense(expense)
        expenses.append(expense)
    return expenses


class edit_expenses:
    def __init__(self, path):
        self.path = Path(path)
        self.expenses = []

    def __enter__(self):
        if self.path.exists():
            self.expenses = load_expenses(self.path)
        return self.expenses

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            save_expenses(self.path, self.expenses)
        return False
