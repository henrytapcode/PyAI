"""Expense tracker, part 2: summing with comprehensions and sorting the finished totals."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Expense:
    date: str
    category: str
    amount: float
    note: str = ""


def totals_by_category(expenses: list[Expense]) -> dict[str, float]:
    names = sorted({expense.category for expense in expenses})
    return {
        name: round(sum(e.amount for e in expenses if e.category == name), 2) for name in names
    }


def totals_by_month(expenses: list[Expense]) -> dict[str, float]:
    months = sorted({expense.date[:7] for expense in expenses})
    return {
        month: round(sum(e.amount for e in expenses if e.date[:7] == month), 2)
        for month in months
    }


def top_category(expenses: list[Expense]) -> str | None:
    totals = totals_by_category(expenses)
    ranking = sorted(totals, key=lambda name: (-totals[name], name))
    return ranking[0] if ranking else None
