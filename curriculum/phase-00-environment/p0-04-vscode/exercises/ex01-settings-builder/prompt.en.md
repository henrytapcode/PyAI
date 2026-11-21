Write two functions in `starter.py` to generate and validate a `.vscode/settings.json` configuration:

1. `build_vscode_settings(venv_path: str, line_length: int = 100, format_on_save: bool = True) -> dict`
   - Strip leading/trailing whitespace from `venv_path`.
   - Raise `ValueError` if `venv_path.strip()` is empty or if `line_length` is outside `[40, 200]` (`not (40 <= line_length <= 200)`).
   - Return a dictionary with these exact keys and values:
     - `"python.defaultInterpreterPath"`: stripped `venv_path`
     - `"editor.formatOnSave"`: `bool(format_on_save)`
     - `"ruff.lineLength"`: `line_length`
     - `"[python]"`: `{"editor.defaultFormatter": "charliermarsh.ruff"}`

2. `validate_settings_json(raw_json: str) -> tuple[bool, list[str]]`
   - Parse `raw_json` with `json.loads()`.
   - If `raw_json` is invalid JSON or the parsed top-level value is not a `dict`, return `(False, ["invalid_json"])`.
   - Otherwise, check required keys in this exact order: `"python.defaultInterpreterPath"`, `"editor.formatOnSave"`, `"[python]"`:
     - For each missing key, append `f"missing:{key}"` to `errors`.
   - After checking missing keys, if `"python.defaultInterpreterPath"` is present in the dict, verify that its value is a `str` with non-empty stripped text (`isinstance(val, str) and val.strip() != ""`). If not, append `"invalid:python.defaultInterpreterPath"` to `errors`.
   - Return `(len(errors) == 0, errors)`.
