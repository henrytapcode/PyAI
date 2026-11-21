# VS Code settings as JSON

**What it shows:** building, serializing, and reading back a `.vscode/settings.json` configuration with Python's `json` module.

**Step by step**
1. Lines 3–8 build a Python `dict` with the four core VS Code settings for `.venv` and Ruff.
2. Line 10 calls `json.dumps(settings, indent=2)` to format the dictionary as readable JSON (converting Python's `True` to JSON's `true`).
3. Lines 13–15 parse the JSON string back with `json.loads()` and verify `editor.formatOnSave` and the Python formatter ID.

**Try it yourself:** change `"ruff.lineLength"` to `88` and run again to see the updated JSON output.
