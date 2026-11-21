import json


def build_vscode_settings(
    venv_path: str, line_length: int = 100, format_on_save: bool = True
) -> dict:
    # TODO: validate inputs and return the VS Code settings dictionary.
    pass


def validate_settings_json(raw_json: str) -> tuple[bool, list[str]]:
    # TODO: parse raw_json with json.loads and return (is_valid, errors).
    pass
