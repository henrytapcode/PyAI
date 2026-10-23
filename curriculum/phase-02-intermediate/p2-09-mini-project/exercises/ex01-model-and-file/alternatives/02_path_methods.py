"""Expense tracker, part 1, using json.dumps / json.loads with Path.write_text / read_text."""
import json
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Expense:
    date: str
    category: str
    amount: float
    note: str = ""


def check_expense(expense: Expense) -> None:
    year, dash1, rest = str(expense.date).partition("-")
    month, dash2, day = rest.partition("-")
    date_ok = (
        isinstance(expense.date, str)
        and dash1 == dash2 == "-"
        and (len(year), len(month), len(day)) == (4, 2, 2)
        and (year + month + day).isdigit()
    )
    if not date_ok:
        raise ValueError(f"date must look like YYYY-MM-DD, got {expense.date!r}")
    if not isinstance(expense.category, str) or not expense.category.strip():
        raise ValueError("category must not be empty")
    if not isinstance(expense.amount, (int, float)) or expense.amount <= 0:
        raise ValueError(f"amount must be a number above 0, got {expense.amount!r}")


def save_expenses(path, expenses: list[Expense]) -> None:
    for expense in expenses:
        check_expense(expense)
    text = json.dumps([asdict(expense) for expense in expenses], indent=2)
    Path(path).write_text(text, encoding="utf-8")


def load_expenses(path) -> list[Expense]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
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
    path = Path(path)
    expenses = load_expenses(path) if path.exists() else []
    yield expenses
    save_expenses(path, expenses)
