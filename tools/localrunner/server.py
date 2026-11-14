"""Local FastAPI runner executing Python code in isolated CPython subprocesses."""

from __future__ import annotations

import asyncio
import codecs
import importlib.metadata
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import AsyncIterator, Sequence
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

RUN_TIMEOUT_S = 120
TEST_TIMEOUT_S = 60
TRACE_TIMEOUT_S = 30

DEFAULT_ORIGINS = ("http://localhost:3000", "http://127.0.0.1:3000")
MAX_FIELD_BYTES = 200 * 1024
MAX_RAW_BODY_BYTES = 512 * 1024
CHILD_SCRIPT = Path(__file__).resolve().parent / "child.py"


def resolve_allowed_origins(extra_origins: Sequence[str] | None = None) -> tuple[str, ...]:
    """Return deduplicated allowed origins from defaults, env, and explicit arguments."""
    candidates: list[str] = list(DEFAULT_ORIGINS)
    env_raw = os.environ.get("PYAI_RUNNER_ORIGINS", "")
    if env_raw:
        candidates.extend(env_raw.split(","))
    if extra_origins:
        candidates.extend(extra_origins)

    seen: set[str] = set()
    result: list[str] = []
    for raw in candidates:
        origin = raw.strip().rstrip("/")
        if origin and origin not in seen:
            seen.add(origin)
            result.append(origin)
    return tuple(result)


def _is_valid_host(host_header: str | None, expected_port: int | None) -> bool:
    if not host_header:
        return False
    host = host_header.strip().lower()
    if expected_port is not None:
        return host in (f"127.0.0.1:{expected_port}", f"localhost:{expected_port}")
    match = re.fullmatch(r"(?:127\.0\.0\.1|localhost):(\d+)", host)
    if not match:
        return False
    port_num = int(match.group(1))
    return 1 <= port_num <= 65535


def _package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def _child_env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    env["MPLBACKEND"] = "Agg"
    env["HF_HUB_OFFLINE"] = "1"
    env["TRANSFORMERS_OFFLINE"] = "1"
    env["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
    return env


def _kill_process(proc: subprocess.Popen[Any]) -> None:
    if proc.poll() is not None:
        return
    try:
        proc.kill()
    except OSError:
        pass
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass


def _close_pipes(proc: subprocess.Popen[Any]) -> None:
    for pipe in (proc.stdin, proc.stdout, proc.stderr):
        if pipe is not None:
            try:
                pipe.close()
            except OSError:
                pass


def _ndjson_line(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")


def _write_stdin(proc: subprocess.Popen[Any], data: bytes) -> None:
    assert proc.stdin is not None
    try:
        proc.stdin.write(data)
        proc.stdin.flush()
    except OSError:
        pass
    finally:
        try:
            proc.stdin.close()
        except OSError:
            pass


def _stream_pipe(
    pipe: Any,
    kind: str,
    loop: asyncio.AbstractEventLoop,
    queue: asyncio.Queue[tuple[str, str]],
) -> None:
    decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
    pending_cr = False
    fd = pipe.fileno()

    def _emit(text: str) -> None:
        if not text:
            return
        try:
            loop.call_soon_threadsafe(queue.put_nowait, (kind, text))
        except RuntimeError:
            pass

    try:
        while True:
            try:
                chunk = os.read(fd, 4096)
            except OSError:
                break
            if not chunk:
                break
            text = decoder.decode(chunk, final=False)
            if pending_cr:
                text = "\r" + text
                pending_cr = False
            if text.endswith("\r"):
                pending_cr = True
                text = text[:-1]
            text = text.replace("\r\n", "\n")
            _emit(text)
        tail = decoder.decode(b"", final=True)
        if pending_cr:
            tail = "\r" + tail
        _emit(tail.replace("\r\n", "\n"))
    finally:
        try:
            loop.call_soon_threadsafe(queue.put_nowait, ("eof", kind))
        except RuntimeError:
            pass


def _drain_pipe(pipe: Any, sink: bytearray, limit: int = 8192) -> None:
    fd = pipe.fileno()
    while True:
        try:
            chunk = os.read(fd, 4096)
        except OSError:
            break
        if not chunk:
            break
        if len(sink) < limit:
            sink.extend(chunk[: limit - len(sink)])


class _SecurityMiddleware:
    """Enforce Host, Origin, X-PyAI-Runner, and CORS with Private Network Access."""

    def __init__(
        self,
        app: Any,
        allowed_origins: tuple[str, ...],
        port: int | None,
    ) -> None:
        self.app = app
        self.allowed_origins = set(allowed_origins)
        self.port = port

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in scope["headers"]}
        if not _is_valid_host(headers.get("host"), self.port):
            await self._send_json(send, 403, {"detail": "Invalid Host header"})
            return

        origin = headers.get("origin")
        if origin is not None and origin not in self.allowed_origins:
            await self._send_json(send, 403, {"detail": "Origin not allowed"})
            return

        method = scope["method"].upper()
        cors_headers: list[tuple[bytes, bytes]] = []
        if origin is not None:
            cors_headers = [
                (b"access-control-allow-origin", origin.encode("latin-1")),
                (b"vary", b"Origin"),
            ]

        if method == "OPTIONS":
            if origin is None:
                await self._send_json(send, 403, {"detail": "Origin required for preflight"})
                return
            preflight_headers = [
                *cors_headers,
                (b"access-control-allow-methods", b"GET, POST"),
                (b"access-control-allow-headers", b"Content-Type, X-PyAI-Runner"),
                (b"access-control-allow-private-network", b"true"),
                (b"content-length", b"0"),
            ]
            await send({"type": "http.response.start", "status": 204, "headers": preflight_headers})
            await send({"type": "http.response.body", "body": b""})
            return

        if method == "POST" and headers.get("x-pyai-runner") != "1":
            await self._send_json(
                send,
                403,
                {"detail": "Missing or invalid X-PyAI-Runner header"},
                extra_headers=cors_headers,
            )
            return

        async def send_with_cors(message: dict[str, Any]) -> None:
            if message["type"] == "http.response.start" and cors_headers:
                message = {**message, "headers": [*message.get("headers", []), *cors_headers]}
            await send(message)

        await self.app(scope, receive, send_with_cors)

    @staticmethod
    async def _send_json(
        send: Any,
        status: int,
        payload: dict[str, Any],
        extra_headers: list[tuple[bytes, bytes]] | None = None,
    ) -> None:
        body = json.dumps(payload).encode("utf-8")
        headers = [
            (b"content-type", b"application/json"),
            (b"content-length", str(len(body)).encode("ascii")),
            *(extra_headers or []),
        ]
        await send({"type": "http.response.start", "status": status, "headers": headers})
        await send({"type": "http.response.body", "body": body})


async def _parse_json_fields(
    request: Request,
    required_fields: tuple[str, ...],
) -> tuple[dict[str, str] | None, JSONResponse | None]:
    content_length = request.headers.get("content-length")
    if content_length is not None:
        try:
            if int(content_length) > MAX_RAW_BODY_BYTES:
                return None, JSONResponse({"detail": "Request body too large"}, status_code=413)
        except ValueError:
            pass

    raw = await request.body()
    if len(raw) > MAX_RAW_BODY_BYTES:
        return None, JSONResponse({"detail": "Request body too large"}, status_code=413)

    try:
        data = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, JSONResponse({"detail": "Invalid JSON body"}, status_code=422)

    if not isinstance(data, dict):
        return None, JSONResponse({"detail": "JSON body must be an object"}, status_code=422)

    parsed: dict[str, str] = {}
    for field in required_fields:
        value = data.get(field)
        if not isinstance(value, str):
            return None, JSONResponse(
                {"detail": f"Field {field!r} must be a string"},
                status_code=422,
            )
        if len(value.encode("utf-8")) > MAX_FIELD_BYTES:
            return None, JSONResponse(
                {"detail": f"Field {field!r} exceeds 200 KB limit"},
                status_code=413,
            )
        parsed[field] = value
    return parsed, None


async def _run_sync_child(
    lock: asyncio.Lock,
    request: Request,
    mode: str,
    payload: dict[str, str],
    timeout_s: float,
    timeout_response: dict[str, Any],
) -> JSONResponse:
    async with lock:
        if await request.is_disconnected():
            return JSONResponse(timeout_response)

        cwd_dir = tempfile.TemporaryDirectory(prefix="pyai-cwd-", ignore_cleanup_errors=True)
        ipc_dir = tempfile.TemporaryDirectory(prefix="pyai-ipc-", ignore_cleanup_errors=True)
        result_path = Path(ipc_dir.name) / "result.json"
        stderr_buf = bytearray()
        proc: subprocess.Popen[bytes] | None = None
        threads: list[threading.Thread] = []

        try:
            proc = subprocess.Popen(
                [
                    sys.executable,
                    "-I",
                    "-u",
                    "-X",
                    "utf8",
                    str(CHILD_SCRIPT),
                    mode,
                    str(result_path),
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                cwd=cwd_dir.name,
                env=_child_env(),
            )
            stdin_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            t_in = threading.Thread(target=_write_stdin, args=(proc, stdin_bytes), daemon=True)
            t_err = threading.Thread(
                target=_drain_pipe, args=(proc.stderr, stderr_buf), daemon=True
            )
            threads = [t_in, t_err]
            for t in threads:
                t.start()

            deadline = time.monotonic() + timeout_s
            while proc.poll() is None:
                if await request.is_disconnected():
                    _kill_process(proc)
                    return JSONResponse(timeout_response)
                if time.monotonic() >= deadline:
                    _kill_process(proc)
                    return JSONResponse(timeout_response)
                await asyncio.sleep(0.05)

            for t in threads:
                t.join(timeout=2)

            if result_path.is_file():
                data = json.loads(result_path.read_text(encoding="utf-8"))
                return JSONResponse(data)

            err_text = stderr_buf.decode("utf-8", errors="replace").strip()
            detail = err_text or f"Runner exited with code {proc.returncode}"
            return JSONResponse({"detail": detail}, status_code=500)
        finally:
            if proc is not None:
                _kill_process(proc)
                _close_pipes(proc)
            for t in threads:
                t.join(timeout=1)
            cwd_dir.cleanup()
            ipc_dir.cleanup()


def create_app(
    allowed_origins: Sequence[str] | None = None,
    port: int | None = None,
    run_timeout: float = RUN_TIMEOUT_S,
    test_timeout: float = TEST_TIMEOUT_S,
    trace_timeout: float = TRACE_TIMEOUT_S,
) -> FastAPI:
    """Create the FastAPI localrunner application."""
    origins = resolve_allowed_origins(allowed_origins)
    app = FastAPI(title="PyAI Local Runner", docs_url=None, redoc_url=None, openapi_url=None)
    run_lock = asyncio.Lock()

    app.add_middleware(_SecurityMiddleware, allowed_origins=origins, port=port)

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "ok": True,
            "protocol": 1,
            "python": platform.python_version(),
            "torch": _package_version("torch"),
            "transformers": _package_version("transformers"),
        }

    @app.post("/run")
    async def run_code(request: Request) -> Any:
        fields, err_resp = await _parse_json_fields(request, ("code",))
        if err_resp is not None:
            return err_resp
        assert fields is not None
        code = fields["code"]

        async def stream() -> AsyncIterator[bytes]:
            async with run_lock:
                if await request.is_disconnected():
                    return

                cwd_dir = tempfile.TemporaryDirectory(
                    prefix="pyai-cwd-", ignore_cleanup_errors=True
                )
                ipc_dir = tempfile.TemporaryDirectory(
                    prefix="pyai-ipc-", ignore_cleanup_errors=True
                )
                result_path = Path(ipc_dir.name) / "result.json"
                proc: subprocess.Popen[bytes] | None = None
                threads: list[threading.Thread] = []

                try:
                    loop = asyncio.get_running_loop()
                    queue: asyncio.Queue[tuple[str, str]] = asyncio.Queue()
                    proc = subprocess.Popen(
                        [
                            sys.executable,
                            "-I",
                            "-u",
                            "-X",
                            "utf8",
                            str(CHILD_SCRIPT),
                            "run",
                            str(result_path),
                        ],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=cwd_dir.name,
                        env=_child_env(),
                    )
                    stdin_bytes = json.dumps({"code": code}, ensure_ascii=False).encode("utf-8")
                    t_in = threading.Thread(
                        target=_write_stdin, args=(proc, stdin_bytes), daemon=True
                    )
                    t_out = threading.Thread(
                        target=_stream_pipe,
                        args=(proc.stdout, "stdout", loop, queue),
                        daemon=True,
                    )
                    t_err = threading.Thread(
                        target=_stream_pipe,
                        args=(proc.stderr, "stderr", loop, queue),
                        daemon=True,
                    )
                    threads = [t_in, t_out, t_err]
                    for t in threads:
                        t.start()

                    deadline = time.monotonic() + run_timeout
                    timed_out = False
                    eof_count = 0

                    while eof_count < 2:
                        if await request.is_disconnected():
                            _kill_process(proc)
                            return
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            timed_out = True
                            _kill_process(proc)
                            break
                        try:
                            kind, text = await asyncio.wait_for(
                                queue.get(), timeout=min(remaining, 0.25)
                            )
                        except TimeoutError:
                            continue
                        if kind == "eof":
                            eof_count += 1
                        elif kind in ("stdout", "stderr"):
                            yield _ndjson_line({"type": kind, "text": text})

                    if not timed_out:
                        while proc.poll() is None:
                            if await request.is_disconnected():
                                _kill_process(proc)
                                return
                            if time.monotonic() >= deadline:
                                timed_out = True
                                _kill_process(proc)
                                break
                            await asyncio.sleep(0.05)

                    for t in threads:
                        t.join(timeout=2)

                    if not timed_out:
                        while not queue.empty():
                            kind, text = queue.get_nowait()
                            if kind in ("stdout", "stderr"):
                                yield _ndjson_line({"type": kind, "text": text})

                    if timed_out:
                        yield _ndjson_line(
                            {"type": "done", "ok": False, "error": None, "timedOut": True}
                        )
                    elif result_path.is_file():
                        data = json.loads(result_path.read_text(encoding="utf-8"))
                        for img in data.get("images", []):
                            yield _ndjson_line({"type": "image", "data": img})
                        yield _ndjson_line(
                            {
                                "type": "done",
                                "ok": bool(data.get("ok", False)),
                                "error": data.get("error"),
                            }
                        )
                    else:
                        yield _ndjson_line(
                            {
                                "type": "done",
                                "ok": False,
                                "error": f"Runner exited unexpectedly (code {proc.returncode})",
                            }
                        )
                finally:
                    if proc is not None:
                        _kill_process(proc)
                        _close_pipes(proc)
                    for t in threads:
                        t.join(timeout=1)
                    cwd_dir.cleanup()
                    ipc_dir.cleanup()

        return StreamingResponse(stream(), media_type="application/x-ndjson")

    @app.post("/test")
    async def test_code(request: Request) -> JSONResponse:
        fields, err_resp = await _parse_json_fields(request, ("code", "tests"))
        if err_resp is not None:
            return err_resp
        assert fields is not None
        return await _run_sync_child(
            lock=run_lock,
            request=request,
            mode="test",
            payload=fields,
            timeout_s=test_timeout,
            timeout_response={
                "ok": False,
                "passed": 0,
                "total": 0,
                "tests": [],
                "error": None,
                "stdout": "",
                "timedOut": True,
            },
        )

    @app.post("/trace")
    async def trace_code(request: Request) -> JSONResponse:
        fields, err_resp = await _parse_json_fields(request, ("code",))
        if err_resp is not None:
            return err_resp
        assert fields is not None
        return await _run_sync_child(
            lock=run_lock,
            request=request,
            mode="trace",
            payload=fields,
            timeout_s=trace_timeout,
            timeout_response={
                "steps": [],
                "stdout": "",
                "error": None,
                "truncated": False,
                "timedOut": True,
            },
        )

    return app
