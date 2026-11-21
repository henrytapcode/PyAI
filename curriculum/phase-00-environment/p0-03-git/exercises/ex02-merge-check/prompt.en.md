Implement two functions to simulate a three-way branch merge and validate commit messages:

1. `three_way_merge(base: dict[str, str], main: dict[str, str], feature: dict[str, str]) -> dict`
   Merge all file paths across `base`, `main`, and `feature` and return `{"merged": dict[str, str], "conflicts": list[str]}`:
   - If `main` and `feature` have the same state for a path (same content, or both absent), keep that state (omit if absent).
   - If one branch matches `base` (unchanged), take the other branch's state (deleting the path from `"merged"` if the changed branch removed it).
   - If both branches changed a path differently from `base` and from each other, add the path to the sorted `"conflicts"` list and keep `main`'s value in `"merged"` if `main` still has the path.

2. `is_valid_commit_msg(msg: str) -> bool`
   Extract the subject line (text before the first `\n`, stripped of leading/trailing whitespace) and return `True` if and only if:
   - The subject is non-empty.
   - `len(subject) <= 72`.
   - The subject does not end with `"."`.
   - The subject starts with an ASCII letter (`a`–`z` or `A`–`Z`).

Press **Check** to run the tests.
