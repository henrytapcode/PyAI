# Index-range loop and Counter

Instead of slicing the shuffled index list into three sublists and building comprehensions, this version walks the permutation once with `enumerate(perm)` and routes each `(text, label)` pair by its position boundary (`pos < n_train` vs. `pos < n_train + n_val`), while using `collections.Counter` for `class_counts`.

The single-pass loop makes split boundaries explicit and avoids creating intermediate index lists, though list comprehensions over slices in `solution.py` are shorter and easier to scan once you are comfortable with Python slicing.
