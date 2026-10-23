Now the report half of the expense tracker. Given a list of `Expense` objects, add them up by category and by month, and find the category where the most money went. `Expense` is already written in the editor. Write your code inside the three functions and `return` the answer. Lesson section 7 shows the accumulator loop and the month slice.

**Example**

```python
expenses = [
    Expense("2024-01-05", "food", 4.5),
    Expense("2024-01-09", "fun", 9.0),
    Expense("2024-02-01", "food", 6.25),
]
totals_by_category(expenses)   # {"food": 10.75, "fun": 9.0}
totals_by_month(expenses)      # {"2024-01": 13.5, "2024-02": 6.25}
top_category(expenses)         # "food"
```

**Rules**

- `totals_by_category(expenses)` returns a dict that maps each category to the sum of its amounts. The keys are in alphabetical order, and every total is rounded to 2 decimals with `round(total, 2)`.
- `totals_by_month(expenses)` does the same for months. The key is the first 7 characters of the date (`"2024-01"`), and the keys are in order from the oldest month to the newest. Totals are rounded to 2 decimals. The same month in two different years gives two different keys.
- `top_category(expenses)` returns the **name** of the category with the biggest total (compare the rounded totals from `totals_by_category`). If two categories have the same biggest total, return the one that comes first in the alphabet. For an empty list return `None`.
- An empty list gives `{}` from the two totals functions.
- All amounts are above `0` (they already passed `check_expense`), so you do not need to check them.
- Do not change the list you receive.

Press **Check** to run the tests.
