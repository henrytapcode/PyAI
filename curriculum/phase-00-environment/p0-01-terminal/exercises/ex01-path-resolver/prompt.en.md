Implement two terminal helper functions in pure Python:

1. `resolve_path(cwd: str, target: str) -> str`:
   - Resolves `target` against `cwd` using POSIX `/` separators.
   - If `target` starts with `"/"`, it is an **absolute** path (ignore `cwd`).
   - Otherwise, it is **relative** to `cwd`.
   - Collapse duplicate slashes (`//`), skip `.`, and pop one directory on `..` (clamping at `"/"` if already at root).
   - Always return a normalized path starting with `"/"` and no trailing slash (except `"/"` itself).

2. `split_command(line: str) -> tuple[str, list[str]]`:
   - Strips leading/trailing whitespace and splits `line` on whitespace.
   - Returns `(cmd, args)` where `cmd` is the first token and `args` is the list of remaining tokens.
   - Raises `ValueError` if `line` is empty or contains only whitespace.

### Examples
```python
resolve_path("/home/alex/app", "../data/./notes.txt")  # "/home/alex/data/notes.txt"
resolve_path("/home/alex", "../../../etc")             # "/etc"
resolve_path("/home/alex", "/var/log//app")            # "/var/log/app"
split_command("  python  main.py --fast ")             # ("python", ["main.py", "--fast"])
```
