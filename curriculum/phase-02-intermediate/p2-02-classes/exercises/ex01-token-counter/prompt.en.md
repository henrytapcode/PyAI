Write a class `TokenCounter` that tracks how many tokens an LLM feature has used. Fill in the four methods. Put your code inside the methods and `return` the answers (do not print them).

**Example**

```python
counter = TokenCounter()
counter.add(10)
counter.add(20)
print(counter.total)       # 30
print(counter.calls)       # 2
print(counter.average())   # 15.0
print(counter)             # TokenCounter(total=30, calls=2)
```

**Rules**
- A new `TokenCounter()` has the attributes `total` and `calls`, both `0`.
- `add(n)` adds `n` to `total` and adds `1` to `calls`. It returns nothing.
- `average()` returns `total / calls`. If `add` was never called, it returns `0`.
- `__repr__` returns the text `TokenCounter(total=30, calls=2)` (with the real numbers) so that `print(counter)` shows it.
- Every counter keeps its own numbers: adding to one counter must not change another.
