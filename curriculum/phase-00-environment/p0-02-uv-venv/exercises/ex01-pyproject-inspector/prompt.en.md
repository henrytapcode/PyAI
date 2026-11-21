Implement two helper functions in `starter.py` using Python's standard library (`tomllib`):

1. **`parse_dependencies(toml_text: str) -> dict[str, str]`**
   - Parse `toml_text` with `tomllib.loads`.
   - Read `[project].dependencies` (return `{}` if `[project]` or `dependencies` is missing).
   - For each dependency string:
     - Support operators `==`, `>=`, `<=`, `~=`, `!=`, `>`, `<`.
     - Strip whitespace around the package name and around the version number (so `"httpx >= 0.27.0"` becomes `"httpx": ">=0.27.0"`).
     - Strip any optional `[extras]` suffix from the package name (so `"requests[security]>=2.31"` becomes `"requests": ">=2.31"`).
     - Lowercase the package name (e.g. `"PyYAML>=6.0"` → `"pyyaml": ">=6.0"`).
     - If there is no version operator (e.g. `"pytest"`), map the name to `""`.

2. **`missing_packages(required: dict[str, str], installed: dict[str, str]) -> list[str]`**
   - Compare package names case-insensitively.
   - Return a sorted list of lowercase package names present in `required` but absent from `installed`.

Press **Check** to run the tests.
