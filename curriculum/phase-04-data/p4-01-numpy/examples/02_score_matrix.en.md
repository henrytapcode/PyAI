# Score matrix

**What it shows:** aggregating a 2D array along `axis=0` (per column) and `axis=1` (per row), then finding the winner with `argmax()`.

**Step by step**
1. Lines 4–10 define four student names and a `(4, 3)` score matrix (4 students × 3 quizzes).
2. Line 12 computes `scores.mean(axis=0)` to average down each column, giving one mean per quiz.
3. Line 13 computes `scores.mean(axis=1)` to average across each row, giving one mean per student.
4. Line 17 calls `student_means.argmax()` to get the index (`2`) of the highest average, and line 18 looks up `"Chi"` in `students`.

**Notice:** `argmax()` returns a position (`2`), not the score (`9.0`). Using `int(...)` turns the NumPy integer into a plain Python `int` for indexing `students`.

**Try it yourself:** change Chi's third score (`8.5` on line 8) to `5.0` and run again to see who becomes the top student.
