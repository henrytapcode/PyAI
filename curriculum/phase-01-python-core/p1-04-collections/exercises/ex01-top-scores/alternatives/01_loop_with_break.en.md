# A loop that stops at n

Instead of slicing, this version walks through the sorted list, adds each score to a new list, and uses `break` to stop as soon as the new list has `n` items. It is longer, but every step is visible, which makes it easy to follow with **Visualize**. The slice `ordered[:n]` does the same job in one line, so prefer it once you are comfortable with slicing.
