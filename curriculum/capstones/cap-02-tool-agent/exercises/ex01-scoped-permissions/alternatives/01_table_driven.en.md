# Table-driven guard pipeline

This alternative extracts each permission, validation, policy, and confirmation check into a pure guard function and orders them in `_GUARD_PIPELINE`. `ScopedRegistry.execute` loops through the pipeline, breaks on the first denial, and appends the `audit_log` entry in a single exit path. Separating the guard table from `execute` makes it easy to unit-test each rule independently or reorder/insert new policy checks without deepening nested conditionals, whereas the linear method in `solution.py` keeps the full priority chain visible in one place.
