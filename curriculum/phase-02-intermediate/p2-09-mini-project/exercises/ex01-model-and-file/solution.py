"""Expense tracker, part 1: the model, the checks and the JSON file."""
import json
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(frozen=True, eq=True)
class Expense:
    date: str
    category: str
    amount: float
    note: str = field(default="")


def is_iso_date(text: object) -> bool:
    if not isinstance(text, str) or len(text) != 10:
        return False
    if text[4] != "-" or text[7] != "-":
        return False
    return (text[:4] + text[5:7] + text[8:]).isdigit()


def check_expense(expense: Expense) -> None:
    if not is_iso_date(expense.date):
        raise ValueError(f"date must look like YYYY-MM-DD, got {expense.date!r}")
    if not isinstance(expense.category, str) or not expense.category.strip():
        raise ValueError("category must not be empty")
    if not isinstance(expense.amount, (int, float)) or expense.amount <= 0:
        raise ValueError(f"amount must be a number above 0, got {expense.amount!r}")


def save_expenses(path, expenses: list[Expense]) -> None:
    for expense in expenses:
        check_expense(expense)
    data = [asdict(expense) for expense in expenses]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


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


@contextmanager
def edit_expenses(path):
    expenses = load_expenses(path) if Path(path).exists() else []
    yield expenses
    save_expenses(path, expenses)
