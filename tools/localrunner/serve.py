"""CLI entrypoint for the local Python runner server."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import uvicorn

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.localrunner.server import create_app, resolve_allowed_origins  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the local CPython execution server bound to 127.0.0.1."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="TCP port to listen on (default: 8765).",
    )
    parser.add_argument(
        "--allow-origin",
        action="append",
        default=[],
        metavar="URL",
        help="Additional allowed browser origin (repeatable).",
    )
    args = parser.parse_args(argv)

    origins = resolve_allowed_origins(args.allow_origin)
    print(
        f"PyAI local runner listening on http://127.0.0.1:{args.port} "
        f"(allowed origins: {', '.join(origins)})",
        flush=True,
    )
    app = create_app(allowed_origins=args.allow_origin, port=args.port)
    uvicorn.run(app, host="127.0.0.1", port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
