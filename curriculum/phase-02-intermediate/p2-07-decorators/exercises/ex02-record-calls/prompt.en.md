The decorator `record_calls` should write each call to the list `CALL_LOG` and then behave exactly like the original function. But functions decorated with it return the wrong things. Run the tests, find the bugs, and fix `record_calls` in the starter code.

**Example**

```python
@record_calls
def add(a, b=0):
    """Add two numbers."""
    return a + b

add(2, 3)      # returns 5, and CALL_LOG is now [("add", (2, 3))]
add(2, b=3)    # returns 5, and CALL_LOG gets ("add", (2,))
```

**Rules**
- Each call adds one tuple `(function name, positional arguments)` to `CALL_LOG`. Keyword arguments are not part of the tuple.
- The decorated function returns whatever the original returns, with every argument passed on.
- The decorated function keeps its original name and docstring.
- Keep the name `CALL_LOG` and the shape of `record_calls`. Only fix the bugs.
