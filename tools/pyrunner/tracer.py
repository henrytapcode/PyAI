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
import sys
import types
from contextlib import redirect_stdout

FILENAME = "<main>"
MAX_STEPS = 600
MAX_REPR = 120
HIDDEN_TYPES = (types.ModuleType,)


class _TooManySteps(Exception):
    pass


def _short(value) -> str:
    try:
        if isinstance(value, types.FunctionType):
            return f"function {value.__name__}()"
        if isinstance(value, type):
            return f"class {value.__name__}"
        if isinstance(value, types.GeneratorType):
            return f"generator {value.__name__}()"
        text = repr(value)
        if " object at 0x" in text and hasattr(value, "__dict__"):
            # Default repr hides the state; show the attributes so learners can watch them change.
            attrs = ", ".join(f"{k}={v!r}" for k, v in vars(value).items())
            text = f"{type(value).__name__}({attrs})"
    except Exception:  # noqa: BLE001 - broken __repr__ in learner code
        text = f"<{type(value).__name__}>"
    return text if len(text) <= MAX_REPR else text[: MAX_REPR - 3] + "..."


def _vars(frame) -> list[dict]:
    items = []
    for name, value in frame.f_locals.items():
        if name.startswith("__") or isinstance(value, HIDDEN_TYPES):
            continue
        items.append({"name": name, "type": type(value).__name__, "repr": _short(value)})
    return items


def _stack(frame) -> list[dict]:
    frames = []
    while frame is not None:
        if frame.f_code.co_filename == FILENAME:
            name = frame.f_code.co_name
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
