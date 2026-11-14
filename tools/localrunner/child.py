"""Subprocess entrypoint for executing learner code in isolation.

Invoked by server.py as:
    python -I child.py <mode> <result_path>
with JSON payload on stdin and structured result written to <result_path>.
"""

from __future__ import annotations

import ast
import base64
import builtins
import io
import json
import linecache
import os
import sys
import traceback
from pathlib import Path

_PYRUNNER_DIR = Path(__file__).resolve().parent.parent / "pyrunner"
if str(_PYRUNNER_DIR) not in sys.path:
    sys.path.insert(0, str(_PYRUNNER_DIR))


def _no_input(prompt: str = "") -> str:
    raise RuntimeError(
        "input() is not available in the editor. Assign a value directly, e.g. name = 'Lan'."
    )


def _uses_matplotlib(code: str) -> bool:
    if not code or "matplotlib" not in code:
        return False
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(
            a.name == "matplotlib" or a.name.startswith("matplotlib.") for a in node.names
        ):
            return True
        if isinstance(node, ast.ImportFrom) and node.module and (
            node.module == "matplotlib" or node.module.startswith("matplotlib.")
        ):
            return True
    return False


def _prepare_mpl() -> None:
    os.environ["MPLBACKEND"] = "Agg"
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.show = lambda *a, **k: None


def _collect_mpl_images() -> list[str]:
    import matplotlib.pyplot as plt

    images: list[str] = []
    try:
        for num in plt.get_fignums():
            fig = plt.figure(num)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
            b64 = base64.b64encode(buf.getvalue()).decode("ascii")
            images.append(f"data:image/png;base64,{b64}")
    finally:
        plt.close("all")
    return images


def _clean_traceback(exc: BaseException) -> str:
    """Keep only learner frames (main.py), hiding child.py and site-packages paths."""
    te = traceback.TracebackException.from_exception(exc)

    def _filter(item: traceback.TracebackException) -> None:
        item.stack = traceback.StackSummary.from_list(
            [frame for frame in item.stack if frame.filename == "main.py"]
        )
        if item.__cause__ is not None:
            _filter(item.__cause__)
        if item.__context__ is not None:
            _filter(item.__context__)
        if getattr(item, "exceptions", None):
            for sub in item.exceptions:
                _filter(sub)

    _filter(te)
    return "".join(te.format()).strip()


def _run_mode(code: str) -> dict:
    import runner

    runner.reset_state()
    builtins.input = _no_input
    has_mpl = _uses_matplotlib(code)
    if has_mpl:
        _prepare_mpl()

    linecache.cache["main.py"] = (len(code), None, code.splitlines(True), "main.py")
    ok = True
    error: str | None = None
    images: list[str] = []
    try:
        compiled = compile(code, "main.py", "exec")
        exec(compiled, {"__name__": "__main__"})
    except BaseException as exc:  # noqa: BLE001 - report learner errors cleanly
        ok = False
        error = _clean_traceback(exc)
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        if has_mpl:
            try:
                images = _collect_mpl_images()
            except Exception:  # noqa: BLE001 - never let figure export hide execution outcome
                pass
    return {"ok": ok, "error": error, "images": images}


def _test_mode(code: str, tests: str) -> dict:
    import runner

    return runner.run_tests(code, tests)


def _trace_mode(code: str) -> dict:
    import runner
    import tracer

    runner.reset_state()
    has_mpl = _uses_matplotlib(code)
    if has_mpl:
        _prepare_mpl()
    try:
        return tracer.trace(code)
    finally:
        if has_mpl:
            try:
                import matplotlib.pyplot as plt

                plt.close("all")
            except Exception:  # noqa: BLE001
                pass


def _configure_stdio() -> None:
    """Ensure UTF-8 and unbuffered streaming even when launched with python -I."""
    for stream, write_through in ((sys.stdin, False), (sys.stdout, True), (sys.stderr, True)):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            kwargs: dict[str, object] = {"encoding": "utf-8"}
            if write_through:
                kwargs["write_through"] = True
            reconfigure(**kwargs)


def main() -> int:
    _configure_stdio()
    if len(sys.argv) != 3:
        sys.stderr.write("usage: child.py <run|test|trace> <result_path>\n")
        return 2

    mode = sys.argv[1]
    result_path = Path(sys.argv[2])
    payload = json.load(sys.stdin)

    if mode == "run":
        result = _run_mode(payload["code"])
    elif mode == "test":
        result = _test_mode(payload["code"], payload["tests"])
    elif mode == "trace":
        result = _trace_mode(payload["code"])
    else:
        sys.stderr.write(f"unknown mode: {mode}\n")
        return 2

    with open(result_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
