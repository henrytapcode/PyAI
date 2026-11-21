import exercise
import pytest


def test_find_python_files_all():
    entries = ["README.md", "/main.py", "src/app.py", "data/notes.txt"]
    assert exercise.find_python_files(entries) == ["main.py", "src/app.py"]


def test_find_python_files_folder_boundary():
    entries = ["src/b.py", "src_old/a.py", "src/utils/io.py", "src/a.py"]
    assert exercise.find_python_files(entries, folder="/src/") == [
        "src/a.py",
        "src/b.py",
        "src/utils/io.py",
    ]


def test_find_python_files_empty_result():
    assert exercise.find_python_files(["docs/guide.md"], folder="src") == []


def test_build_run_cmd_uv_with_args():
    assert exercise.build_run_cmd(" src/app.py ", ["--port", "8000"], use_uv=True) == [
        "uv",
        "run",
        "python",
        "src/app.py",
        "--port",
        "8000",
    ]


def test_build_run_cmd_plain_python_no_args():
    assert exercise.build_run_cmd("hello.py", use_uv=False) == ["python", "hello.py"]


def test_build_run_cmd_non_py_raises():
    with pytest.raises(ValueError):
        exercise.build_run_cmd("README.md")
