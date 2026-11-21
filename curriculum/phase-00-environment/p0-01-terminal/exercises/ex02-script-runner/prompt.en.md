Implement two script-runner helper functions in pure Python:

1. `find_python_files(entries: list[str], folder: str = "") -> list[str]`:
   - Strips whitespace and leading `"/"` from each entry in `entries`, and keeps only entries ending with `".py"`.
   - Normalizes `folder` by stripping whitespace and leading/trailing `"/"`.
   - If `folder` is non-empty, keeps only `.py` entries inside that folder on a `"/"` boundary (so `folder="src"` matches `"src/app.py"` and `"src/utils/io.py"`, but **never** `"src_old/a.py"`).
   - Returns the matching normalized paths sorted ascending.

2. `build_run_cmd(script: str, args: list[str] | None = None, use_uv: bool = True) -> list[str]`:
   - Strips whitespace from `script`; raises `ValueError` if it does not end with `".py"`.
   - Returns `["uv", "run", "python", script, *args]` when `use_uv=True`, or `["python", script, *args]` when `use_uv=False` (with `args` omitted if `None` or empty).

### Examples
```python
find_python_files(["src/b.py", "src_old/a.py", "src/a.py", "README.md"], folder="src/")
# ["src/a.py", "src/b.py"]

build_run_cmd("src/app.py", ["--port", "8000"], use_uv=True)
# ["uv", "run", "python", "src/app.py", "--port", "8000"]
```
