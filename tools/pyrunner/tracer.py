"""Step-by-step execution trace for the "Visualize" view (like Python Tutor, much smaller).

Runs in Pyodide (loaded by apps/web/public/pyodide-worker.js) and in CPython (tested by
tools/validate.py on every lesson example). ``trace_json(code)`` returns JSON:

  {"steps": [{"line", "event", "stack": [{"name", "vars": [{"name", "type", "repr"}]}], "out", "ret"?}],
   "stdout": "...", "error": {"type", "message", "line"} | null, "truncated": bool}

``out`` is the length of stdout printed before the step, so the UI can slice ``stdout``.
"""

from __future__ import annotations

import io
import json
import math
import sys
import types
from contextlib import redirect_stdout

FILENAME = "<main>"
MAX_STEPS = 600
MAX_REPR = 120
MAX_TABLE_ROWS = 8
MAX_TABLE_COLS = 6
MAX_CELL_CHARS = 24
HIDDEN_TYPES = (types.ModuleType,)


class _TooManySteps(Exception):
    pass


def _repr(value, depth: int = 0) -> str:
    """repr() that shows object state instead of memory addresses, also inside containers."""
    if isinstance(value, types.FunctionType):
        return f"function {value.__name__}()"
    if isinstance(value, type):
        return f"class {value.__name__}"
    if isinstance(value, types.GeneratorType):
        # A suspended generator keeps its locals; show them so "the state is kept" is visible.
        frame = value.gi_frame
        local = ", ".join(f"{k}={_repr(v, depth + 1)}" for k, v in frame.f_locals.items()) if frame else ""
        return f"generator {value.__name__}({local})"
    if depth < 3:
        if type(value) is list:
            return "[" + ", ".join(_repr(v, depth + 1) for v in value) + "]"
        if type(value) is tuple and len(value) != 1:
            return "(" + ", ".join(_repr(v, depth + 1) for v in value) + ")"
        if type(value) is dict:
            return "{" + ", ".join(f"{_repr(k, depth + 1)}: {_repr(v, depth + 1)}" for k, v in value.items()) + "}"
    text = repr(value)
    if " object at 0x" in text and hasattr(value, "__dict__"):
        # Default repr hides the state; show the attributes so learners can watch them change.
        attrs = ", ".join(f"{k}={_repr(v, depth + 1)}" for k, v in vars(value).items())
        text = f"{type(value).__name__}({attrs})"
    return text


def _short(value) -> str:
    try:
        # A learner's __repr__ may print; that must not leak into the program output.
        with redirect_stdout(io.StringIO()):
            text = _repr(value)
    except Exception:  # noqa: BLE001 - broken __repr__ in learner code
        text = f"<{type(value).__name__}>"
    return text if len(text) <= MAX_REPR else text[: MAX_REPR - 3] + "..."


def _cell(value) -> str:
    if (
        type(value).__module__ == "numpy"
        and getattr(value, "ndim", None) == 0
        and hasattr(value, "item")
    ):
        value = value.item()
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        text = format(value, ".6g")
    else:
        text = str(value)
    return text if len(text) <= MAX_CELL_CHARS else text[: MAX_CELL_CHARS - 1] + "…"


def _table(value) -> dict | None:
    cls = type(value)
    cls_name = cls.__name__
    if cls_name not in ("DataFrame", "Series", "ndarray"):
        return None
    mod = cls.__module__
    is_df = cls_name == "DataFrame" and mod.startswith("pandas")
    is_series = cls_name == "Series" and mod.startswith("pandas")
    is_array = cls_name == "ndarray" and mod == "numpy"
    if not (is_df or is_series or is_array):
        return None

    try:
        with redirect_stdout(io.StringIO()):
            if is_df:
                n_rows, n_cols = value.shape
                sub = value.iloc[:MAX_TABLE_ROWS, :MAX_TABLE_COLS]
                return {
                    "kind": "dataframe",
                    "shape": [int(n_rows), int(n_cols)],
                    "columns": [str(c) for c in sub.columns],
                    "index": [str(i) for i in sub.index],
                    "rows": [
                        [_cell(v) for v in row]
                        for row in sub.itertuples(index=False, name=None)
                    ],
                }
            if is_series:
                n_rows = len(value)
                sub = value.iloc[:MAX_TABLE_ROWS]
                col = "" if value.name is None else str(value.name)
                return {
                    "kind": "series",
                    "shape": [int(n_rows), 1],
                    "columns": [col],
                    "index": [str(i) for i in sub.index],
                    "rows": [[_cell(v)] for v in sub],
                }
            if getattr(value, "ndim", None) != 2:
                return None
            n_rows, n_cols = value.shape
            sub = value[:MAX_TABLE_ROWS, :MAX_TABLE_COLS]
            r_lim, c_lim = sub.shape
            return {
                "kind": "array",
                "shape": [int(n_rows), int(n_cols)],
                "columns": [str(i) for i in range(c_lim)],
                "index": [str(i) for i in range(r_lim)],
                "rows": [[_cell(v) for v in row] for row in sub],
            }
    except Exception:  # noqa: BLE001 - broken pandas/numpy repr or object __str__ must never crash trace
        return None


def _vars(frame) -> list[dict]:
    items = []
    for name, value in frame.f_locals.items():
        if name.startswith("__") or isinstance(value, HIDDEN_TYPES):
            continue
        entry: dict = {"name": name, "type": type(value).__name__, "repr": _short(value)}
        table = _table(value)
        if table is not None:
            entry["table"] = table
        items.append(entry)
    return items


def _stack(frame) -> list[dict]:
    frames = []
    while frame is not None:
        if frame.f_code.co_filename == FILENAME:
            name = getattr(frame.f_code, "co_qualname", frame.f_code.co_name).replace(".<locals>", "")
            frames.append({"name": "global" if name == "<module>" else name, "vars": _vars(frame)})
        frame = frame.f_back
    return frames[::-1]


def trace(code: str, max_steps: int = MAX_STEPS) -> dict:
    out = io.StringIO()
    steps: list[dict] = []
    result: dict = {"steps": steps, "stdout": "", "error": None, "truncated": False}

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != FILENAME:
            return None
        if event in ("line", "return", "exception"):
            if len(steps) >= max_steps:
                raise _TooManySteps
            step = {"line": frame.f_lineno, "event": event, "stack": _stack(frame), "out": len(out.getvalue())}
            if event == "return":
                step["ret"] = _short(arg)
            elif event == "exception":
                step["ret"] = f"{arg[0].__name__}: {arg[1]}"
            steps.append(step)
        return tracer

    try:
        compiled = compile(code, FILENAME, "exec")
    except SyntaxError as exc:
        result["error"] = {"type": "SyntaxError", "message": exc.msg, "line": exc.lineno}
        return result

    env = {"__name__": "__main__", "__builtins__": __builtins__}
    old = sys.gettrace()
    try:
        with redirect_stdout(out):
            sys.settrace(tracer)
            try:
                exec(compiled, env)
            finally:
                sys.settrace(old)
    except _TooManySteps:
        result["truncated"] = True
    except BaseException as exc:  # noqa: BLE001 - report learner errors, never crash the UI
        line = None
        tb = exc.__traceback__
        while tb is not None:
            if tb.tb_frame.f_code.co_filename == FILENAME:
                line = tb.tb_lineno
            tb = tb.tb_next
        result["error"] = {"type": type(exc).__name__, "message": str(exc), "line": line}
    result["stdout"] = out.getvalue()[-20000:]
    return result


def trace_json(code: str) -> str:
    return json.dumps(trace(code), ensure_ascii=False)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        print(json.dumps(trace(f.read()), ensure_ascii=False, indent=2))
