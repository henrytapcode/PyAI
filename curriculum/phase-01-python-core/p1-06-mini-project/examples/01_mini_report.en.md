# A tiny grade report

**What it shows:** the whole project in miniature: two small functions, a list of dicts and one loop that ties them together.

**Step by step**
1. Lines 2–5 define `average`. Line 3 checks for an empty list first, so we never divide by zero. Line 5 adds the scores and divides by how many there are.
2. Lines 8–13 define `letter_grade`. Python checks the `if` lines from top to bottom and the first true one returns. That is why one comparison per line is enough.
3. Lines 16–19 store the data: a list with one dict per student. Each dict has a `"name"` and a list of `"scores"`.
4. Line 21 starts the loop, one student at a time. Line 22 reads that student's scores with `student["scores"]` and turns them into an average.
5. Line 23 builds the output line. `{avg:.2f}` shows two decimals and `letter_grade(avg)` is called right inside the f-string.

**Notice:** `average` and `letter_grade` know nothing about students or dicts. They only take a number or a list. That is why you can test them on their own and reuse them anywhere.

**Try it yourself:** add `{"name": "Chi", "scores": [5, 6, 4.5]}` to the list. Predict the new line before you run it (it should print `Chi: 5.17 (C or below)`).
