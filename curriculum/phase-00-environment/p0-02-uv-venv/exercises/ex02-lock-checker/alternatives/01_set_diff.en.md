# Generator lookup & set algebra

This alternative uses `next(..., None)` to find the matching package case-insensitively without allocating an intermediate lowercase dictionary, and computes `diff_lockfiles` with set algebra (`new_keys - old_keys`, `old_keys - new_keys`, `old_keys & new_keys`). Both implementations return the same result; set operators make the three diff categories immediately obvious when comparing two lockfiles.
