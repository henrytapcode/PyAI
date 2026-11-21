import json


def build_vscode_settings(
    venv_path: str, line_length: int = 100, format_on_save: bool = True
) -> dict:
    trimmed = venv_path.strip()
    if trimmed == "" or line_length < 40 or line_length > 200:
        raise ValueError("Invalid VS Code settings parameters")
    return {
        "python.defaultInterpreterPath": trimmed,
        "editor.formatOnSave": bool(format_on_save),
        "ruff.lineLength": line_length,
        "[python]": {"editor.defaultFormatter": "charliermarsh.ruff"},
    }


def validate_settings_json(raw_json: str) -> tuple[bool, list[str]]:
    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError:
        return False, ["invalid_json"]

    if type(parsed) is not dict:
        return False, ["invalid_json"]

    errors: list[str] = []
    if "python.defaultInterpreterPath" not in parsed:
        errors.append("missing:python.defaultInterpreterPath")
    if "editor.formatOnSave" not in parsed:
        errors.append("missing:editor.formatOnSave")
    if "[python]" not in parsed:
        errors.append("missing:[python]")

    if "python.defaultInterpreterPath" in parsed:
        value = parsed["python.defaultInterpreterPath"]
        if type(value) is not str or value.strip() == "":
            errors.append("invalid:python.defaultInterpreterPath")

    return len(errors) == 0, errors
