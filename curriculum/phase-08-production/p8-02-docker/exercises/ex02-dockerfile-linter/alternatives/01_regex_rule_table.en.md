# Regex parsing with a declarative rule table

This alternative folds `\` line continuations and extracts `(INSTRUCTION, args)` with `re` instead of a manual character buffer, then stores each check in a `RULES` list of `(code, check_fn)` pairs. Choose this rule-table design when a team plans to add many lint checks or toggle rules from configuration, and choose the explicit `if` statements in `solution.py` when you only have a handful of fixed checks and want zero indirection while debugging.
