import exercise
import pytest


def test_resolve_relative_path():
    assert exercise.resolve_path("/home/alex/app", "src/main.py") == "/home/alex/app/src/main.py"


def test_resolve_dot_and_parent():
    got = exercise.resolve_path("/home/alex/app", "../data/./notes.txt")
    assert got == "/home/alex/data/notes.txt"


def test_resolve_clamps_at_root():
    assert exercise.resolve_path("/home/alex", "../../../../etc") == "/etc"
    assert exercise.resolve_path("/home", "../..") == "/"


def test_resolve_absolute_and_duplicate_slashes():
    assert exercise.resolve_path("/home/alex", "/var//log/app/") == "/var/log/app"


def test_split_command_with_args():
    assert exercise.split_command("  python  main.py --fast ") == ("python", ["main.py", "--fast"])


def test_split_command_no_args():
    assert exercise.split_command("pwd") == ("pwd", [])


def test_split_command_blank_raises():
    with pytest.raises(ValueError):
        exercise.split_command("   ")
