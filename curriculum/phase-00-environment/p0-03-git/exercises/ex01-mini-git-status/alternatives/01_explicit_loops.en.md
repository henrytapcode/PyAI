# Explicit loops and set difference

This alternative builds `untracked` and `modified` in a single sorted pass over `working`, and computes `deleted` with a set difference `set(staged) - set(working)`.
