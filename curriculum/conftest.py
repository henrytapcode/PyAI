"""Make every exercises/*/test_exercise.py import the code under test as ``exercise``.

EXERCISE_TARGET=solution (default) -> loads solution.py
EXERCISE_TARGET=starter            -> loads starter.py (should FAIL)
"""

import importlib.util
import os
import sys

import pytest

# Force non-interactive backend so matplotlib never opens GUI windows during pytest.
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")


class ExerciseModule(pytest.Module):
    def _getobj(self):
        target = os.environ.get("EXERCISE_TARGET", "solution")
        path = self.path.parent / f"{target}.py"
        spec = importlib.util.spec_from_file_location("exercise", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["exercise"] = module
        spec.loader.exec_module(module)
        return super()._getobj()


def pytest_pycollect_makemodule(module_path, parent):
    if module_path.name == "test_exercise.py":
        return ExerciseModule.from_parent(parent, path=module_path)
    return None
