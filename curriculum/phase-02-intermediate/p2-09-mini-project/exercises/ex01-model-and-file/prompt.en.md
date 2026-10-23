Build the first half of the expense tracker: the `Expense` model, a checker that refuses bad data, two functions that save a list of expenses to a JSON file and load it back, and a context manager that edits the saved list safely. The editor already holds a skeleton with `# TODO` steps. Write your code inside the class and the functions, and add helper functions if you like. Lesson sections 2 to 5 show every tool you need.

**Example**

```python
lunch = Expense("2024-03-05", "food", 4.5, "pho")
save_expenses("e.json", [lunch])
load_expenses("e.json")            # [Expense(date='2024-03-05', category='food', amount=4.5, note='pho')]
check_expense(Expense("2024-3-5", "food", 4.5))   # raises ValueError (bad date)

with edit_expenses("e.json") as expenses:
    expenses.append(Expense("2024-03-06", "fun", 9.0))
# the file now holds two expenses
```

**Rules**

- `Expense` is a **frozen** dataclass with the fields `date`, `category`, `amount` and `note`, in that order. `note` is optional and defaults to `""`.
- `check_expense(expense)` returns `None` when the expense is fine, and raises `ValueError` when any rule is broken:
  - `date` is text in the form `YYYY-MM-DD`: three parts split by `-`, with 4, 2 and 2 digits;
  - `category` is text that is not empty after `strip()`;
  - `amount` is a number (`int` or `float`) greater than `0`.
  - A `date` or `category` that is not text at all (for example the number `20240305`) also raises `ValueError`.
- `save_expenses(path, expenses)` first checks **every** expense. If one is bad it raises `ValueError` and does **not** create or change the file. Otherwise it writes a JSON list with one object per expense, using the keys `date`, `category`, `amount` and `note`.
- `load_expenses(path)` returns a list of `Expense` objects, in file order:
  - a missing file raises `FileNotFoundError`;
  - text that is not JSON, a JSON value that is not a list, a record that is not an object with the right keys (missing or extra keys), and a record that breaks a rule of `check_expense` all raise `ValueError`.
- Saving and then loading must give back equal expenses.
- `edit_expenses(path)` is a context manager written with `@contextmanager`. It loads the expenses of `path` and gives that list to the `with` block (`as expenses`). A missing file starts as `[]`. When the block ends **without an error**, it saves the list with `save_expenses`, so every expense is checked first. If the block raises an error, or an expense in the list is bad, the file stays exactly as it was.

Press **Check** to run the tests.
