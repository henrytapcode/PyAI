# Let range skip the odd numbers

Instead of checking every number with `if number % 2 == 0`, start at 2 and use `step = 2`: `range(2, n + 1, 2)` only produces 2, 4, 6, ... so every number is already even. There is no `if` at all, and the loop does half the work. The idea is the same accumulator pattern; you only changed which numbers the loop visits.
