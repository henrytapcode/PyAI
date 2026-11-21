import json

REQUIRED_KEYS = (
    "python.defaultInterpreterPath",
    "editor.formatOnSave",
    "[python]",
)


def build_vscode_settings(
    venv_path: str, line_length: int = 100, format_on_save: bool = True
) -> dict:
    cleaned_path = venv_path.strip()
    if not cleaned_path:
        raise ValueError("venv_path must not be empty")
    if not (40 <= line_length <= 200):
        raise ValueError("line_length must be between 40 and 200")
    return {
        "python.defaultInterpreterPath": cleaned_path,
        "editor.formatOnSave": bool(format_on_save),
        "ruff.lineLength": line_length,
        "[python]": {"editor.defaultFormatter": "charliermarsh.ruff"},
    }


def validate_settings_json(raw_json: str) -> tuple[bool, list[str]]:
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError:
        return (False, ["invalid_json"])

    if not isinstance(data, dict):
        return (False, ["invalid_json"])

    errors: list[str] = []
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"missing:{key}")

    if "python.defaultInterpreterPath" in data:
        interp = data["python.defaultInterpreterPath"]
        if not isinstance(interp, str) or not interp.strip():
            errors.append("invalid:python.defaultInterpreterPath")

    return (len(errors) == 0, errors)
