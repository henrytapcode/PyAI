"""Tiny pytest-compatible test runner.

Runs in two places with identical behaviour:
  * in the browser, inside Pyodide (apps/web loads this file as a string), and
  * in CPython, from tools/validate.py, to prove every exercise works in the browser.

Supported pytest subset: plain ``assert`` (with operand introspection), ``pytest.raises``,
``pytest.approx``, ``pytest.mark.parametrize`` and the ``capsys`` fixture.
Student code is loaded as the module ``exercise``; tests do ``from exercise import ...``.
"""

from __future__ import annotations

import ast
import inspect
import io
import json
import linecache
import re
import sys
import traceback
import types
from contextlib import redirect_stderr, redirect_stdout

EXERCISE_FILE = "<exercise.py>"
TEST_FILE = "<test_exercise.py>"


# ---------------------------------------------------------------- pytest shim
class _RaisesContext:
    def __init__(self, expected, match=None):
        self.expected = expected
        self.match = match
        self.value = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        name = getattr(self.expected, "__name__", str(self.expected))
        if exc_type is None:
            raise AssertionError(f"DID NOT RAISE {name}")
        if not issubclass(exc_type, self.expected):
            return False
        if self.match is not None and not re.search(self.match, str(exc)):
            raise AssertionError(f"{name} raised, but message {str(exc)!r} does not match {self.match!r}")
        self.value = exc
        return True


class _Approx:
    def __init__(self, expected, rel=1e-6, abs=1e-12):
        self.expected, self.rel, self.abs = expected, rel, abs

    def _close(self, a, b):
        return abs(a - b) <= max(self.rel * abs(b), self.abs)

    def __eq__(self, other):
        exp = self.expected
        if isinstance(exp, (list, tuple)):
            return len(other) == len(exp) and all(self._close(a, b) for a, b in zip(other, exp))
        return self._close(other, exp)

    def __repr__(self):
        return f"approx({self.expected!r})"


class _Mark:
    def parametrize(self, argnames, argvalues, ids=None):
        names = [n.strip() for n in argnames.split(",")] if isinstance(argnames, str) else list(argnames)

        def deco(fn):
            fn.__dict__.setdefault("_params", []).append((names, list(argvalues), ids))
            return fn

        return deco

    def __getattr__(self, _name):  # pytest.mark.slow etc. -> no-op decorator
        return lambda *a, **k: (a[0] if a and callable(a[0]) else (lambda f: f))


def _make_pytest_shim():
    mod = types.ModuleType("pytest")
    mod.raises = lambda expected, match=None: _RaisesContext(expected, match)
    mod.approx = _Approx
    mod.mark = _Mark()
    mod.fixture = lambda *a, **k: (a[0] if a and callable(a[0]) else (lambda f: f))
    mod.__file__ = "<pytest-shim>"
    return mod


class _CaptureResult(tuple):
    @property
    def out(self):
        return self[0]

    @property
    def err(self):
        return self[1]


class _Capsys:
    def __init__(self, out: io.StringIO, err: io.StringIO):
        self._out, self._err = out, err
        self._o = self._e = 0

    def readouterr(self):
        out, err = self._out.getvalue(), self._err.getvalue()
        res = _CaptureResult((out[self._o:], err[self._e:]))
        self._o, self._e = len(out), len(err)
        return res


# ---------------------------------------------------------------- helpers
def _load_module(name: str, source: str, filename: str):
    linecache.cache[filename] = (len(source), None, source.splitlines(True), filename)
    mod = types.ModuleType(name)
    mod.__file__ = filename
    sys.modules[name] = mod
    exec(compile(source, filename, "exec"), mod.__dict__)
    return mod


def _humanize(name: str) -> str:
    return name.removeprefix("test_").replace("_", " ").strip() or name


_OPS = {
    ast.Eq: "==", ast.NotEq: "!=", ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">=",
    ast.In: "in", ast.NotIn: "not in", ast.Is: "is", ast.IsNot: "is not",
}


def _short_repr(value, limit: int = 160) -> str:
    text = repr(value)
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _explain_assert(tb, test_source: str) -> tuple[str | None, int | None]:
    """Re-evaluate a failing ``assert a <op> b`` to show both sides, like pytest does."""
    frame, lineno = None, None
    for fr, ln in traceback.walk_tb(tb):
        if fr.f_code.co_filename == TEST_FILE:
            frame, lineno = fr, ln
    if frame is None:
        return None, None
    try:
        tree = ast.parse(test_source)
    except SyntaxError:
        return None, lineno
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert) and node.lineno <= lineno <= (node.end_lineno or node.lineno):
            src = ast.get_source_segment(test_source, node.test) or ""
            test = node.test
            if isinstance(test, ast.Compare) and len(test.ops) == 1 and type(test.ops[0]) in _OPS:
                try:
                    env = dict(frame.f_globals)
                    env.update(frame.f_locals)
                    left = eval(compile(ast.Expression(test.left), TEST_FILE, "eval"), env)
                    right = eval(compile(ast.Expression(test.comparators[0]), TEST_FILE, "eval"), env)
                    left_src = ast.get_source_segment(test_source, test.left) or "left"
                    op = _OPS[type(test.ops[0])]
                    return f"assert {src}\n  {left_src} = {_short_repr(left)}\n  expected {op} {_short_repr(right)}", node.lineno
                except Exception:  # noqa: BLE001 - best effort only
                    pass
            return f"assert {src}", node.lineno
    return None, lineno


def _student_line(tb) -> int | None:
    line = None
    for fr, ln in traceback.walk_tb(tb):
        if fr.f_code.co_filename == EXERCISE_FILE:
            line = ln
    return line


def _collect(test_mod):
    cases = []
    for name, fn in list(vars(test_mod).items()):
        if not (name.startswith("test") and inspect.isfunction(fn)):
            continue
        if fn.__code__.co_filename != TEST_FILE:
            continue
        params = fn.__dict__.get("_params")
        if not params:
            cases.append((name, fn, {}))
            continue
        # Cartesian product of stacked parametrize decorators.
        combos = [({}, "")]
        for names, values, ids in params:
            new = []
            for i, value in enumerate(values):
                vals = value if len(names) > 1 else (value,)
                label = ids[i] if ids else "-".join(_short_repr(v, 20) for v in vals)
                for base, base_label in combos:
                    merged = dict(base)
                    merged.update(zip(names, vals))
                    new.append((merged, f"{base_label}-{label}" if base_label else label))
            combos = new
        for kwargs, label in combos:
            cases.append((f"{name}[{label}]", fn, kwargs))
    return cases


# ---------------------------------------------------------------- public API
def run_tests(user_code: str, test_code: str) -> dict:
    out, err = io.StringIO(), io.StringIO()
    result: dict = {"ok": False, "passed": 0, "total": 0, "tests": [], "error": None, "stdout": ""}
    saved = {k: sys.modules.get(k) for k in ("pytest", "exercise", "test_exercise")}
    sys.modules["pytest"] = _make_pytest_shim()
    try:
        with redirect_stdout(out), redirect_stderr(err):
            try:
                _load_module("exercise", user_code, EXERCISE_FILE)
            except SyntaxError as exc:
                result["error"] = {"type": "SyntaxError", "message": exc.msg, "line": exc.lineno}
                return result
            except BaseException as exc:  # noqa: BLE001
                result["error"] = {
                    "type": type(exc).__name__,
                    "message": str(exc),
                    "line": _student_line(exc.__traceback__),
                }
                return result
            test_mod = _load_module("test_exercise", test_code, TEST_FILE)
            cases = _collect(test_mod)
            for name, fn, kwargs in cases:
                call_kwargs = dict(kwargs)
                if "capsys" in inspect.signature(fn).parameters:
                    call_kwargs["capsys"] = _Capsys(out, err)
                entry = {"name": name, "label": _humanize(name), "status": "passed", "message": None, "line": None}
                try:
                    fn(**call_kwargs)
                except AssertionError as exc:
                    detail, line = _explain_assert(exc.__traceback__, test_code)
                    entry.update(status="failed", line=line)
                    msg = str(exc)
                    entry["message"] = "\n".join(p for p in (msg, detail) if p) or "assertion failed"
                except BaseException as exc:  # noqa: BLE001
                    entry.update(
                        status="error",
                        message=f"{type(exc).__name__}: {exc}",
                        line=_student_line(exc.__traceback__),
                    )
                result["tests"].append(entry)
        result["total"] = len(result["tests"])
        result["passed"] = sum(t["status"] == "passed" for t in result["tests"])
        result["ok"] = result["total"] > 0 and result["passed"] == result["total"]
        return result
    finally:
        result["stdout"] = out.getvalue()[-20000:]
        for key, value in saved.items():
            if value is None:
                sys.modules.pop(key, None)
            else:
                sys.modules[key] = value


def run_tests_json(user_code: str, test_code: str) -> str:
    return json.dumps(run_tests(user_code, test_code), ensure_ascii=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: runner.py <exercise.py> <test_exercise.py>")
        raise SystemExit(2)
    with open(sys.argv[1], encoding="utf-8") as f_code, open(sys.argv[2], encoding="utf-8") as f_test:
        print(json.dumps(run_tests(f_code.read(), f_test.read()), ensure_ascii=False, indent=2))
