# PyAI Local Runner

Local FastAPI server that executes learner Python code (`torch`, `transformers`, `FastAPI`, etc.) in isolated CPython subprocesses for exercises marked `runner: local`.

## Running

```bash
uv run python tools/localrunner/serve.py
```

Options:

- `--port 8765` — port to listen on (default: `8765`)
- `--allow-origin URL` — additional allowed browser origin (repeatable)

You can also add comma-separated origins via `PYAI_RUNNER_ORIGINS`.

## Security

Because the server executes arbitrary Python code on the learner's machine:

1. Binds strictly to `127.0.0.1` (no `--host` flag).
2. Validates the `Host` header (`127.0.0.1:<port>` or `localhost:<port>`) to block DNS rebinding.
3. Rejects any request with an `Origin` outside the allowlist (`http://localhost:3000`, `http://127.0.0.1:3000`, plus `PYAI_RUNNER_ORIGINS` / `--allow-origin`).
4. Requires `X-PyAI-Runner: 1` on all `POST` requests so browsers must send a CORS preflight.
5. Restricts CORS to allowed origins, `GET`/`POST`, `Content-Type`/`X-PyAI-Runner`, and sets `Access-Control-Allow-Private-Network: true` on valid preflights.
6. Caps `code` and `tests` fields at 200 KB each (`413` on overflow), runs each request sequentially (`asyncio.Lock`) in `python -I` inside a temporary `cwd` with `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`, and kills the subprocess on timeout or client disconnect.

## Endpoints

- `GET /health` — returns `{"ok", "protocol", "python", "torch", "transformers"}` without importing `torch`.
- `POST /run` — body `{"code": str}`; streams NDJSON messages (`stdout`, `stderr`, `image`, and final `done` with optional `timedOut: true`).
- `POST /test` — body `{"code": str, "tests": str}`; returns JSON matching `tools/pyrunner/runner.py`.
- `POST /trace` — body `{"code": str}`; returns JSON matching `tools/pyrunner/tracer.py`.
