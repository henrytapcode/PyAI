After every experiment you report a few numbers about your scores. The standard library already has the tools, so import them instead of writing the maths yourself. Write two functions inside the file and `return` the answers.

1. `summarize(values)` takes a list of at least two numbers and returns a dict with the keys `"count"`, `"mean"`, `"median"` and `"stdev"`. Round `"stdev"` to 2 decimals; leave the others as they come.
2. `same_average(a, b)` takes two lists of numbers and returns `True` when their averages are equal for practical purposes, `False` otherwise.

**Example**

| Call | Result |
|---|---|
| `summarize([70, 80, 90, 100])` | `{"count": 4, "mean": 85, "median": 85.0, "stdev": 12.91}` |
| `same_average([0.1, 0.2], [0.15])` | `True` |
| `same_average([1, 2, 3], [5])` | `False` |

**Rules**
- Use `statistics` for the summary and `math.isclose` to compare the averages.
- Put the `import` lines at the top of the file.
- `return` the values, do not `print` them.
