# A log file that always closes

**What it shows:** a context manager written as a class. It opens a log file when the block starts and closes it when the block ends, with or without an error.

**Step by step**
1. Lines 6–8 save the path in `__init__`. The file is not opened yet.
2. Lines 10–13 are `__enter__`: it opens the file and returns `self`, so `as run` gives you the manager.
3. Lines 15–16 are a normal method, `log`, that writes one line.
4. Lines 18–21 are `__exit__`: it closes the file and returns `False`, so errors are not hidden.
5. Lines 27–30 use the manager normally. Lines 32–38 use it again and crash inside the block; the file is closed anyway and the error reaches `except`.
6. Lines 40–41 read the file back. Opening it with `"w"` the second time replaced the first content.

**Notice:** `closed: True` is printed both times. `run.file.closed` is checked after the `with` block, when the file is already closed.

**Try it yourself:** change `"w"` to `"a"` on line 11. The final line should now show all three messages.
