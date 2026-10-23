Four functions below have a type hint, and each hint is supposed to describe the function truthfully. They are buggy: in three of them the **hint** is wrong, and in one the **code** is wrong. Run the tests, find which is which, and fix it. The docstrings describe the correct behaviour.

**Example**

```python
average_length(["ab", "abcd"])   # 3.0   (a float, not an int)
find_system([])                  # None  (nothing found)
repeat("ab", 2)                  # "abab"
shout("hi")                      # "HI"
```

**Rules**
- Keep the function names and parameter names.
- Fix a hint when the code is right and the hint lies. Fix the code when the code does not do what its docstring says.
- Do not change what `find_system` returns when there is no system message: it must still be `None`.
- The tests check both the results and the hints: they read `__annotations__` the way a type checker would.
