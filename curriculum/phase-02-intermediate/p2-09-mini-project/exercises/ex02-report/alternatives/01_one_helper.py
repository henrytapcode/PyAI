"""Expense tracker, part 2: both totals functions share one helper that takes a key function."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Expense:
    date: str
    category: str
    amount: float
    note: str = ""


def group_totals(expenses: list[Expense], key_of) -> dict[str, float]:
    totals = {}
    for expense in expenses:
        key = key_of(expense)
        totals[key] = totals.get(key, 0) + expense.amount
    return {key: round(totals[key], 2) for key in sorted(totals)}


def category_of(expense: Expense) -> str:
    return expense.category


def month_of(expense: Expense) -> str:
    return expense.date[:7]


def totals_by_category(expenses: list[Expense]) -> dict[str, float]:
    return group_totals(expenses, category_of)


def totals_by_month(expenses: list[Expense]) -> dict[str, float]:
    return group_totals(expenses, month_of)


def top_category(expenses: list[Expense]) -> str | None:
    totals = totals_by_category(expenses)
    if not totals:
        return None
    return max(totals, key=totals.get)
