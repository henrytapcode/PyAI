import exercise


def test_parse_dependencies_standard():
    toml_text = """
[project]
name = "demo"
dependencies = [
    "PyYAML>=6.0",
    "httpx == 0.27.0",
    "pytest",
]
"""
    assert exercise.parse_dependencies(toml_text) == {
        "pyyaml": ">=6.0",
        "httpx": "==0.27.0",
        "pytest": "",
    }


def test_parse_dependencies_extras_and_operators():
    toml_text = """
[project]
dependencies = [
    "requests[security] >= 2.31",
    "pydantic~=2.6",
    "numpy!=1.25.0",
    "rich<14.0",
    "typing-extensions>4.0",
    "click<=8.1.7",
]
"""
    assert exercise.parse_dependencies(toml_text) == {
        "requests": ">=2.31",
        "pydantic": "~=2.6",
        "numpy": "!=1.25.0",
        "rich": "<14.0",
        "typing-extensions": ">4.0",
        "click": "<=8.1.7",
    }


def test_parse_dependencies_missing_sections():
    assert exercise.parse_dependencies("") == {}
    assert exercise.parse_dependencies('[project]\nname = "empty"\n') == {}


def test_missing_packages_case_insensitive_sorted():
    required = {"PyYAML": ">=6.0", "HTTPX": ">=0.27", "pytest": ""}
    installed = {"pyyaml": "6.0.1"}
    assert exercise.missing_packages(required, installed) == ["httpx", "pytest"]


def test_missing_packages_none_missing():
    required = {"Httpx": ">=0.27"}
    installed = {"httpx": "0.27.2", "rich": "13.7.0"}
    assert exercise.missing_packages(required, installed) == []
