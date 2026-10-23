# A class with `__enter__` and `__exit__`

The same `edit_expenses`, written the long way from the context managers lesson. `__enter__` loads the list (or starts with `[]`) and returns it, so it becomes the name after `as`. `__exit__` receives the error details: when `exc_type` is `None` the block finished well, so it saves; otherwise it does nothing, and `return False` lets the error continue. If a saved expense is bad, `save_expenses` raises `ValueError` inside `__exit__` and the file stays as it was.

The class is the better choice when the manager needs to keep more state or has several methods. For a short "set up, yield, tear down" job like this one, the `@contextmanager` generator in the main solution is shorter and easier to read.
