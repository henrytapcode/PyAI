Now the statistics for the whole class. `average` and `letter_grade` are already written in the starter. Complete `class_stats(students)`. Write your code inside the function and `return` the answer.

It returns a dict with these keys:

| Key | Value |
|---|---|
| `"count"` | number of students |
| `"mean"` | the mean of all students' averages |
| `"best"` | the **name** of the student with the highest average |
| `"worst"` | the **name** of the student with the lowest average |
| `"grade_counts"` | a dict with **all five** letters `"A"` to `"F"` and how many students got each (0 if none) |

Edge cases:

- Find best and worst with a loop. If several students tie for best (or worst), pick the one whose name comes first alphabetically.
- A student with an empty `scores` list has average `0.0` (grade `"F"`).
- For an empty class: `{"count": 0, "mean": 0.0, "best": None, "worst": None, "grade_counts": {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}}`.

Example:

```python
class_stats([
    {"name": "An", "scores": [8, 7.5, 9]},
    {"name": "Binh", "scores": [9, 9.5, 8.5]},
])
# {"count": 2, "mean": 8.583..., "best": "Binh", "worst": "An",
#  "grade_counts": {"A": 1, "B": 1, "C": 0, "D": 0, "F": 0}}
```

Press **Check** to run the tests.
