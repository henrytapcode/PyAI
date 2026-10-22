Ms. Lan stores each student as a dict like `{"name": "An", "scores": [8, 7.5, 9]}`. Complete the three functions. Write your code inside the functions and `return` the answer.

1. `average(scores)` returns the mean of a list of numbers. For an empty list it returns `0.0`.
2. `letter_grade(avg)` returns a letter on a 10-point scale:
   - `"A"` if `avg >= 8.5`, `"B"` if `avg >= 7`, `"C"` if `avg >= 5.5`, `"D"` if `avg >= 4`, otherwise `"F"`.
3. `build_report(students)` returns a **list of strings**, one per student, like `"An: 8.17 (B)"`:
   - the average is shown with exactly 2 decimals;
   - students are sorted by average, highest first; students with the same average are sorted by name (A to Z);
   - an empty class gives an empty list `[]`.

Example:

```python
build_report([
    {"name": "An", "scores": [8, 7.5, 9]},
    {"name": "Binh", "scores": [9, 9.5, 8.5]},
])
# ["Binh: 9.00 (A)", "An: 8.17 (B)"]
```

Press **Check** to run the tests.
