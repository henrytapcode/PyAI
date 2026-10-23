"""Expense tracker, part 2: the report."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Expense:
    date: str
    category: str
    amount: float
    note: str = ""


def totals_by_category(expenses: list[Expense]) -> dict[str, float]:
    totals = {}
    for expense in expenses:
        totals[expense.category] = totals.get(expense.category, 0) + expense.amount
    return {category: round(totals[category], 2) for category in sorted(totals)}


def totals_by_month(expenses: list[Expense]) -> dict[str, float]:
    totals = {}
    for expense in expenses:
        month = expense.date[:7]
        totals[month] = totals.get(month, 0) + expense.amount
    return {month: round(totals[month], 2) for month in sorted(totals)}


def top_category(expenses: list[Expense]) -> str | None:
    totals = totals_by_category(expenses)
    best = None
    best_total = 0
    for category in totals:
        if totals[category] > best_total:
            best = category
            best_total = totals[category]
    return best
