# Deadlines, paths and the `__main__` guard

**What it shows:** date arithmetic with `datetime`, a first look at `pathlib`, and the `if __name__ == "__main__":` pattern used in nearly every real script.

**Step by step**
1. Lines 2–3 import names with `from ... import ...`: `date` and `timedelta` from `datetime`, `Path` from `pathlib`.
2. Lines 6–7: subtracting two dates gives a `timedelta`; its `.days` is a plain whole number.
3. Lines 10–12: `Path("data/raw/reviews.csv")` understands a file path. `.stem` is the name without the extension, `.suffix` is the extension, `.parts` is a tuple of the path pieces. Nothing is read from disk: this only works on the text of the path.
4. Lines 15–23 are `main()`. Line 17 adds a `timedelta(days=45)` to a date: 1 March plus 45 days is 15 April. Line 20 turns the date into the weekday name (`%A` means "full weekday name"). Line 22 joins path pieces with `/`.
5. Lines 26–27: `__name__` is `"__main__"` only when this file is the one you run. If another file did `import` on it, `main()` would **not** run and the functions would simply become available.

**Notice:** the functions on top do work and return values; `main()` does the printing. That split makes the functions easy to reuse and to test.

**Try it yourself:** change the start date or the `45`, and predict the new deadline before you run it.
