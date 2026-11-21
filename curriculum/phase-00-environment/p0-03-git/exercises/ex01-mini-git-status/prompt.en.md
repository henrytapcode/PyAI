Implement two functions that simulate Git's status check and staging area using dictionaries mapping file paths to file contents:

1. `git_status(committed: dict[str, str], staged: dict[str, str], working: dict[str, str]) -> dict[str, list[str]]`
   Return a dictionary with four **sorted** lists of file paths:
   - `"staged"`: paths where `staged.get(p) != committed.get(p)` (added, modified, or deleted in `staged` relative to `committed`).
   - `"untracked"`: paths in `working` that are in neither `committed` nor `staged`.
   - `"modified"`: paths in `working` that also exist in `staged` with `working[p] != staged[p]`.
   - `"deleted"`: paths in `staged` that are absent from `working`.

2. `stage_files(staged: dict[str, str], working: dict[str, str], paths: list[str]) -> dict[str, str]`
   Return a **new** `staged` dictionary (never mutating the input `staged`) after staging each path in `paths`:
   - If the path exists in `working`, copy `working[p]` into the new staged dict.
   - If the path is absent from `working` but exists in `staged`, remove it from the new staged dict.
   - If the path is absent from both `working` and `staged`, raise `KeyError`.

Press **Check** to run the tests.
