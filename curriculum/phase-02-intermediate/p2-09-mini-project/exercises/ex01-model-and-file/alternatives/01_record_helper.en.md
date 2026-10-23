# A helper and a list comprehension

This version moves the "one record to one `Expense`" work into its own function, `record_to_expense`, which also does the `TypeError` to `ValueError` conversion. Then `load_expenses` becomes a single list comprehension. The date check is also written another way: it compares the list of part lengths with `[4, 2, 2]`, and joins the parts to test `isdigit()` once. In `edit_expenses`, a missing file is handled by catching `FileNotFoundError` instead of asking `exists()` first.

It is the better choice when the same conversion is needed in more than one place, and the small functions are easy to test alone. For one use, the loop with `try/except` inside `load_expenses` is just as good and keeps everything in one place. Asking `exists()` first (main solution) reads more simply for a missing file, but the `try/except` version also covers a file that disappears between the two steps.
