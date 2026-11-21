import json

import exercise
import pytest


def test_build_vscode_settings_defaults():
    result = exercise.build_vscode_settings("  .venv/bin/python  ")
    assert result == {
        "python.defaultInterpreterPath": ".venv/bin/python",
        "editor.formatOnSave": True,
        "ruff.lineLength": 100,
        "[python]": {"editor.defaultFormatter": "charliermarsh.ruff"},
    }


def test_build_vscode_settings_custom_values():
    result = exercise.build_vscode_settings(
        ".venv\\Scripts\\python.exe", line_length=88, format_on_save=False
    )
    assert result["python.defaultInterpreterPath"] == ".venv\\Scripts\\python.exe"
    assert result["ruff.lineLength"] == 88
    assert result["editor.formatOnSave"] is False


def test_build_vscode_settings_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        exercise.build_vscode_settings("   ")
    with pytest.raises(ValueError):
        exercise.build_vscode_settings(".venv/bin/python", line_length=39)
    with pytest.raises(ValueError):
        exercise.build_vscode_settings(".venv/bin/python", line_length=201)


def test_validate_settings_json_valid():
    raw = json.dumps(exercise.build_vscode_settings(".venv/bin/python"))
    assert exercise.validate_settings_json(raw) == (True, [])


def test_validate_settings_json_invalid_syntax_or_non_dict():
    assert exercise.validate_settings_json("{bad json") == (False, ["invalid_json"])
    assert exercise.validate_settings_json("[1, 2, 3]") == (False, ["invalid_json"])


def test_validate_settings_json_missing_keys_order():
    ok, errors = exercise.validate_settings_json('{"ruff.lineLength": 100}')
    assert ok is False
    assert errors == [
        "missing:python.defaultInterpreterPath",
        "missing:editor.formatOnSave",
        "missing:[python]",
    ]


def test_validate_settings_json_invalid_interpreter():
    raw = json.dumps(
        {
            "python.defaultInterpreterPath": "   ",
            "editor.formatOnSave": True,
            "[python]": {"editor.defaultFormatter": "charliermarsh.ruff"},
        }
    )
    assert exercise.validate_settings_json(raw) == (
        False,
        ["invalid:python.defaultInterpreterPath"],
    )

    raw_non_str = json.dumps(
        {
            "python.defaultInterpreterPath": 123,
            "editor.formatOnSave": True,
            "[python]": {"editor.defaultFormatter": "charliermarsh.ruff"},
        }
    )
    assert exercise.validate_settings_json(raw_non_str) == (
        False,
        ["invalid:python.defaultInterpreterPath"],
    )
