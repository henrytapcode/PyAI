"""Tiny pytest-compatible test runner.

Runs in two places with identical behaviour:
  * in the browser, inside Pyodide (apps/web loads this file as a string), and
  * in CPython, from tools/validate.py, to prove every exercise works in the browser.

Supported pytest subset: plain ``assert`` (with operand introspection), ``pytest.raises``,
``pytest.approx``, ``pytest.mark.parametrize``, ``pytest.fail``, the built-in fixtures ``capsys``,
``tmp_path``, ``caplog`` and ``monkeypatch``, and ``@pytest.fixture`` functions defined in the test
file (including ``yield`` fixtures with teardown).
Student code is loaded as the module ``exercise``; tests do ``from exercise import ...``.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import io
import json
import linecache
import logging
import os
import pathlib
import re
import shutil
import sys
import tempfile
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


def _fixture(*args, **_kwargs):
    def mark(fn):
        fn._pyai_fixture = True
        return fn

    return mark(args[0]) if args and callable(args[0]) else mark


def _fail(reason: str = "", pytrace: bool = True):  # noqa: ARG001 - pytest signature
    raise AssertionError(reason or "failed")


def _make_pytest_shim():
    mod = types.ModuleType("pytest")
    mod.raises = lambda expected, match=None: _RaisesContext(expected, match)
    mod.approx = _Approx
    mod.mark = _Mark()
    mod.fixture = _fixture
    mod.fail = _fail
    mod.MonkeyPatch = _MonkeyPatch
    mod.LogCaptureFixture = _Caplog
    mod.CaptureFixture = _Capsys
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
        # Start from the current end so each test only sees its own output.
        self._o, self._e = len(out.getvalue()), len(err.getvalue())

    def readouterr(self):
        out, err = self._out.getvalue(), self._err.getvalue()
        res = _CaptureResult((out[self._o:], err[self._e:]))
        self._o, self._e = len(out), len(err)
        return res


class _ListHandler(logging.Handler):
    def __init__(self):
        super().__init__(level=0)
        self.records: list[logging.LogRecord] = []
        self.setFormatter(logging.Formatter("%(levelname)-8s %(name)s:%(filename)s:%(lineno)d %(message)s"))

    def emit(self, record):
        self.records.append(record)


class _Caplog:
    """Subset of pytest's ``caplog``: records, messages, text, record_tuples, clear, set_level, at_level."""

    def __init__(self):
        self.handler = _ListHandler()
        self._restore: list[tuple[logging.Logger, int]] = []
        logging.getLogger().addHandler(self.handler)

    @property
    def records(self):
        return self.handler.records

    @property
    def messages(self):
        return [r.getMessage() for r in self.records]

    @property
    def record_tuples(self):
        return [(r.name, r.levelno, r.getMessage()) for r in self.records]

    @property
    def text(self):
        return "\n".join(self.handler.format(r) for r in self.records) + ("\n" if self.records else "")

    def clear(self):
        self.handler.records.clear()

    def set_level(self, level, logger=None):
        lg = logging.getLogger(logger)
        self._restore.append((lg, lg.level))
        lg.setLevel(level)

    def at_level(self, level, logger=None):
        caplog = self

        class _Ctx:
            def __enter__(self):
                lg = logging.getLogger(logger)
                self.lg, self.old = lg, lg.level
                lg.setLevel(level)
                return caplog

            def __exit__(self, *exc):
                self.lg.setLevel(self.old)
                return False

        return _Ctx()

    def _finish(self):
        logging.getLogger().removeHandler(self.handler)
        for lg, level in reversed(self._restore):
            lg.setLevel(level)


_NOTSET = object()


class _MonkeyPatch:
    """Subset of pytest's ``monkeypatch``; everything is undone after the test."""

    def __init__(self):
        self._undo: list = []

    @staticmethod
    def _resolve(dotted: str):
        module_name, _, attr = dotted.rpartition(".")
        parts = module_name.split(".")
        for i in range(len(parts), 0, -1):
            try:
                obj = importlib.import_module(".".join(parts[:i]))
            except ImportError:
                continue
            for part in parts[i:]:
                obj = getattr(obj, part)
            return obj, attr
        raise AttributeError(f"cannot resolve {dotted!r}")

    def setattr(self, target, name, value=_NOTSET, raising=True):
        if value is _NOTSET:
            if not isinstance(target, str):
                raise TypeError("use monkeypatch.setattr(obj, 'name', value)")
            value = name
            target, name = self._resolve(target)
        old = getattr(target, name, _NOTSET)
        if raising and old is _NOTSET:
            raise AttributeError(f"{target!r} has no attribute {name!r}")
        self._undo.append(lambda: delattr(target, name) if old is _NOTSET else setattr(target, name, old))
        setattr(target, name, value)

    def delattr(self, target, name=_NOTSET, raising=True):
        if name is _NOTSET:
            target, name = self._resolve(target)
        if not hasattr(target, name):
            if raising:
                raise AttributeError(name)
            return
        old = getattr(target, name)
        self._undo.append(lambda: setattr(target, name, old))
        delattr(target, name)

    def setitem(self, mapping, key, value):
        old = mapping.get(key, _NOTSET)
        self._undo.append(lambda: mapping.pop(key, None) if old is _NOTSET else mapping.__setitem__(key, old))
        mapping[key] = value

    def delitem(self, mapping, key, raising=True):
        if key not in mapping:
            if raising:
                raise KeyError(key)
            return
        old = mapping[key]
        self._undo.append(lambda: mapping.__setitem__(key, old))
        del mapping[key]

    def setenv(self, name, value, prepend=None):
        value = str(value)
        if prepend and name in os.environ:
            value = value + prepend + os.environ[name]
        self.setitem(os.environ, name, value)

    def delenv(self, name, raising=True):
        self.delitem(os.environ, name, raising)

    def chdir(self, path):
        old = os.getcwd()
        self._undo.append(lambda: os.chdir(old))
        os.chdir(path)

    def undo(self):
        while self._undo:
            self._undo.pop()()


class _FixtureError(Exception):
    pass


def _resolve_fixture(name, test_mod, cache, cleanups, out, err, chain=()):
    if name in cache:
        return cache[name]
    if name in chain:
        raise _FixtureError(f"recursive fixture {name!r}")
    if name == "capsys":
        value = _Capsys(out, err)
    elif name == "tmp_path":
        value = pathlib.Path(tempfile.mkdtemp(prefix="pyai-"))
        cleanups.append(lambda p=value: shutil.rmtree(p, ignore_errors=True))
    elif name == "caplog":
        value = _Caplog()
        cleanups.append(value._finish)
    elif name == "monkeypatch":
        value = _MonkeyPatch()
        cleanups.append(value.undo)
    else:
        fn = getattr(test_mod, name, None)
        if not getattr(fn, "_pyai_fixture", False):
            raise _FixtureError(f"fixture {name!r} not found")
        kwargs = {
            p: _resolve_fixture(p, test_mod, cache, cleanups, out, err, (*chain, name))
            for p in inspect.signature(fn).parameters
        }
        if inspect.isgeneratorfunction(fn):
            gen = fn(**kwargs)
            value = next(gen)
            cleanups.append(lambda g=gen: next(g, None))
        else:
            value = fn(**kwargs)
    cache[name] = value
    return value


def _logging_snapshot():
    root = logging.getLogger()
    return root, list(root.handlers), root.level, logging.root.manager.disable


def _logging_restore(snapshot):
    root, handlers, level, disable = snapshot
    root.handlers[:] = handlers
    root.setLevel(level)
    logging.disable(disable)


def reset_state():
    """Called by the browser before each run so logging setup from a previous run does not leak."""
    root = logging.getLogger()
    root.handlers[:] = []
    root.setLevel(logging.WARNING)
    logging.disable(logging.NOTSET)


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
        if not (name.startswith("test") and inspect.isfunction(fn)) or getattr(fn, "_pyai_fixture", False):
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
    log_state = _logging_snapshot()
    cwd = os.getcwd()
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
                entry = {"name": name, "label": _humanize(name), "status": "passed", "message": None, "line": None}
                cleanups: list = []
                try:
                    cache: dict = {}
                    for param in inspect.signature(fn).parameters:
                        if param not in call_kwargs:
                            call_kwargs[param] = _resolve_fixture(param, test_mod, cache, cleanups, out, err)
                    fn(**call_kwargs)
                except _FixtureError as exc:
                    entry.update(status="error", message=f"fixture error: {exc}")
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
                finally:
                    for undo in reversed(cleanups):
                        try:
                            undo()
                        except Exception:  # noqa: BLE001 - teardown must not hide the test result
                            pass
                result["tests"].append(entry)
        result["total"] = len(result["tests"])
        result["passed"] = sum(t["status"] == "passed" for t in result["tests"])
        result["ok"] = result["total"] > 0 and result["passed"] == result["total"]
        return result
    finally:
        _logging_restore(log_state)
        if os.getcwd() != cwd:
            os.chdir(cwd)
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
