Ms. Lan stores each student as a dict like `{"name": "An", "scores": [8, 7.5, 9]}`. Your job is to build the first half of her grade-report tool: the average, the letter grade, and a ranked report. The editor already contains four function skeletons with `# TODO` steps. Write your code inside the functions and `return` the answer. Lesson sections 4 and 5 show the two tricks you need: `:.2f` and `sorted(..., key=...)`.

**Example**

```python
build_report([
    {"name": "An", "scores": [8, 7.5, 9]},
    {"name": "Binh", "scores": [9, 9.5, 8.5]},
])
# ["Binh: 9.00 (A)", "An: 8.17 (B)"]
```

| Function | Input | Output |
|---|---|---|
| `average([5, 6])` | list of numbers | `5.5` |
| `letter_grade(7.2)` | a number | `"B"` |
| `sort_key({"name": "An", "avg": 8.5})` | a row dict | `(-8.5, "An")` |
| `build_report(students)` | list of student dicts | list of text lines |

**Rules**

- `average(scores)` returns the mean of a list of numbers. For an empty list it returns `0.0`.
- `letter_grade(avg)` uses a 10-point scale: `"A"` if `avg >= 8.5`, `"B"` if `avg >= 7`, `"C"` if `avg >= 5.5`, `"D"` if `avg >= 4`, otherwise `"F"`.
- `sort_key(row)` is the sorting helper. `row` is a dict like `{"name": "An", "avg": 8.17}`. Return the tuple `(-row["avg"], row["name"])`.
- `build_report(students)` returns a **list of strings**, one per student, like `"An: 8.17 (B)"`:
  - the average is shown with exactly 2 decimals;
  - students are sorted by average, highest first; students with the same average are sorted by name (A to Z);
  - an empty class gives an empty list `[]`;
  - return the lines, do not print them.

Press **Check** to run the tests.
