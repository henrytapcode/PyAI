# Comprehensions and a sort key

First find the distinct names with a sorted set comprehension, then build each total with `sum(...)` over a generator expression that filters one group. For the top category, `sorted(totals, key=...)` sorts the names with a tuple key `(-total, name)`, exactly like the ranking in the grade-report project, and takes the first one. (`lambda name: ...` is a tiny one-line function with no name, which is a preview of a later topic.)

It reads nicely and has no accumulator, but it goes through the whole list once **per group**, so it slows down when there are many groups. The single-pass loop of the main solution is the better choice for big lists.
