# Reading pyproject.toml with tomllib

**What it shows:** how `uv` stores project metadata and dependencies in `pyproject.toml`, and how Python 3.11+ parses it with `tomllib`.

**Step by step**
1. Lines 4–14 hold a sample `pyproject.toml` as a multi-line string.
2. Line 16 calls `tomllib.loads(...)` to turn the TOML text into nested Python dictionaries and lists.
3. Lines 19–23 read `name`, `requires-python`, and loop through `dependencies`.

**Notice:** `tomllib` is part of the Python standard library—no `uv add` is needed to read a `pyproject.toml` file.

**Try it yourself:** add `"pytest>=8.0"` to `dependencies` and run again.
