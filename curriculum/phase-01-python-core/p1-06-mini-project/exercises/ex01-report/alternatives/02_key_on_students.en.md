# Sort the students directly

Here there is no list of `rows`. The key function `student_key` takes a student dict and computes the average itself, so `sorted(students, key=student_key)` sorts the original dicts. Then the loop computes the average a second time to build each line.

It is shorter, but `average` runs twice per student. For a class of 30 that does not matter; for big data you would rather compute each average once, as in the main solution. The rows approach is also easier to debug, because you can `print(rows)` and see exactly what is being sorted.
