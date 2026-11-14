"""Tests for the local CPython runner server."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from fastapi.testclient import TestClient

from tools.localrunner.server import MAX_FIELD_BYTES, create_app
from tools.pyrunner import runner, tracer

BASE_URL = "http://127.0.0.1:8765"
HEADERS = {"X-PyAI-Runner": "1"}


def _client(app=None) -> TestClient:
    return TestClient(app or create_app(), base_url=BASE_URL)


def _parse_ndjson(text: str) -> list[dict]:
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def test_health():
    client = _client()
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert data["protocol"] == 1
    assert isinstance(data["python"], str) and data["python"]
    assert isinstance(data["torch"], str) and data["torch"]
    assert "torch" not in sys.modules


def test_run_stdout_order_and_done():
    client = _client()
    resp = client.post("/run", json={"code": 'print("a"); print("b")'}, headers=HEADERS)
    assert resp.status_code == 200
    msgs = _parse_ndjson(resp.text)
    stdout = "".join(m["text"] for m in msgs if m["type"] == "stdout")
    assert "a" in stdout and "b" in stdout
    assert stdout.index("a") < stdout.index("b")
    assert msgs[-1] == {"type": "done", "ok": True, "error": None}


def test_run_error_cleans_traceback():
    client = _client()
    resp = client.post("/run", json={"code": "1 / 0"}, headers=HEADERS)
    assert resp.status_code == 200
    msgs = _parse_ndjson(resp.text)
    done = msgs[-1]
    assert done["type"] == "done"
    assert done["ok"] is False
    assert "ZeroDivisionError" in done["error"]
    assert "main.py" in done["error"]
    assert "child.py" not in done["error"]


def test_run_matplotlib_image():
    code = """
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [2, 4, 6])
plt.show()
"""
    client = _client()
    resp = client.post("/run", json={"code": code}, headers=HEADERS)
    assert resp.status_code == 200
    msgs = _parse_ndjson(resp.text)
    images = [m for m in msgs if m["type"] == "image"]
    assert len(images) == 1
    assert images[0]["data"].startswith("data:image/png;base64,")
    assert msgs[-1] == {"type": "done", "ok": True, "error": None}


def test_run_json_like_stdout_does_not_break_protocol():
    code = 'print(\'{"type":"done","ok":false}\')'
    client = _client()
    resp = client.post("/run", json={"code": code}, headers=HEADERS)
    assert resp.status_code == 200
    msgs = _parse_ndjson(resp.text)
    done_msgs = [m for m in msgs if m["type"] == "done"]
    assert len(done_msgs) == 1
    assert done_msgs[0] == {"type": "done", "ok": True, "error": None}
    stdout = "".join(m["text"] for m in msgs if m["type"] == "stdout")
    assert '{"type":"done","ok":false}' in stdout


def test_run_timeout():
    client = _client(create_app(run_timeout=2))
    started = time.monotonic()
    resp = client.post("/run", json={"code": "while True: pass"}, headers=HEADERS)
    elapsed = time.monotonic() - started
    assert resp.status_code == 200
    assert elapsed < 5.0
    msgs = _parse_ndjson(resp.text)
    assert msgs[-1] == {"type": "done", "ok": False, "error": None, "timedOut": True}


def test_run_input_raises_clear_error():
    client = _client()
    resp = client.post("/run", json={"code": "x = input('name: ')"}, headers=HEADERS)
    assert resp.status_code == 200
    msgs = _parse_ndjson(resp.text)
    done = msgs[-1]
    assert done["ok"] is False
    assert "input() is not available in the editor" in done["error"]
    assert "child.py" not in done["error"]


def test_child_env_and_isolated_cwd():
    code = """
import os
print(os.environ.get("HF_HUB_OFFLINE"))
print(os.environ.get("TRANSFORMERS_OFFLINE"))
print(os.getcwd())
"""
    repo_root = str(Path(__file__).resolve().parents[2].resolve())
    client = _client()
    resp = client.post("/run", json={"code": code}, headers=HEADERS)
    assert resp.status_code == 200
    msgs = _parse_ndjson(resp.text)
    assert msgs[-1]["ok"] is True
    lines = "".join(m["text"] for m in msgs if m["type"] == "stdout").strip().splitlines()
    assert lines[0] == "1"
    assert lines[1] == "1"
    assert str(Path(lines[2]).resolve()) != repo_root


def test_test_endpoint_matches_runner():
    code = "def add(a, b):\n    return a + b\n"
    tests = "from exercise import add\n\ndef test_add():\n    assert add(2, 3) == 5\n"
    expected = runner.run_tests(code, tests)

    client = _client()
    resp = client.post("/test", json={"code": code, "tests": tests}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json() == expected


def test_trace_endpoint_matches_tracer():
    code = "x = 1\ny = x + 1"
    expected = tracer.trace(code)

    client = _client()
    resp = client.post("/trace", json={"code": code}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json() == expected


def test_run_torch():
    code = "import torch\nprint(torch.tensor([1, 2]).sum().item())\n"
    client = _client()
    resp = client.post("/run", json={"code": code}, headers=HEADERS)
    assert resp.status_code == 200
    msgs = _parse_ndjson(resp.text)
    assert msgs[-1] == {"type": "done", "ok": True, "error": None}
    stdout = "".join(m["text"] for m in msgs if m["type"] == "stdout")
    assert stdout.strip() == "3"


def test_security_headers_and_cors(monkeypatch):
    client = _client()

    # Missing X-PyAI-Runner header on POST -> 403
    resp = client.post("/run", json={"code": "print(1)"})
    assert resp.status_code == 403

    # Disallowed Origin -> 403
    resp = client.get("/health", headers={"Origin": "https://evil.example"})
    assert resp.status_code == 403

    # Disallowed Host -> 403
    resp = client.get("/health", headers={"Host": "evil.example"})
    assert resp.status_code == 403

    # Valid preflight from http://localhost:3000
    resp = client.options(
        "/run",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type, x-pyai-runner",
        },
    )
    assert resp.status_code in (200, 204)
    assert resp.headers.get("access-control-allow-origin") == "http://localhost:3000"
    assert resp.headers.get("access-control-allow-private-network") == "true"

    # Disallowed preflight has no Access-Control-Allow-Origin
    resp = client.options(
        "/run",
        headers={
            "Origin": "https://evil.example",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert "access-control-allow-origin" not in resp.headers

    # PYAI_RUNNER_ORIGINS adds allowed origins
    monkeypatch.setenv("PYAI_RUNNER_ORIGINS", "https://learner.github.io")
    custom_client = _client(create_app())
    resp = custom_client.get("/health", headers={"Origin": "https://learner.github.io"})
    assert resp.status_code == 200
    assert resp.headers.get("access-control-allow-origin") == "https://learner.github.io"


def test_body_size_limit_returns_413():
    client = _client()
    oversized = "x" * (MAX_FIELD_BYTES + 1)
    resp = client.post("/run", json={"code": oversized}, headers=HEADERS)
    assert resp.status_code == 413

    resp = client.post("/test", json={"code": "x = 1", "tests": oversized}, headers=HEADERS)
    assert resp.status_code == 413


def test_test_and_trace_timeouts_and_port_host_check():
    app = create_app(port=8765, test_timeout=1, trace_timeout=1)
    client = TestClient(app, base_url=BASE_URL)

    # Wrong port in Host header when port is pinned -> 403
    resp = client.get("/health", headers={"Host": "127.0.0.1:9999"})
    assert resp.status_code == 403

    # /test timeout
    resp = client.post(
        "/test",
        json={"code": "while True: pass", "tests": "def test_x(): pass"},
        headers=HEADERS,
    )
    assert resp.status_code == 200
    assert resp.json() == {
        "ok": False,
        "passed": 0,
        "total": 0,
        "tests": [],
        "error": None,
        "stdout": "",
        "timedOut": True,
    }

    # /trace timeout
    resp = client.post("/trace", json={"code": "import time\ntime.sleep(5)"}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json() == {
        "steps": [],
        "stdout": "",
        "error": None,
        "truncated": False,
        "timedOut": True,
    }


def test_run_stderr_streaming():
    client = _client()
    resp = client.post(
        "/run",
        json={"code": "import sys; sys.stderr.write('warn\\n')"},
        headers=HEADERS,
    )
    assert resp.status_code == 200
    msgs = _parse_ndjson(resp.text)
    stderr = "".join(m["text"] for m in msgs if m["type"] == "stderr")
    assert "warn" in stderr
    assert msgs[-1] == {"type": "done", "ok": True, "error": None}


def test_run_utf8_and_incremental_streaming():
    client = _client()
    code = (
        "import time\n"
        "print('Xin chào')\n"
        "time.sleep(0.5)\n"
        "print('Tạm biệt')\n"
    )
    timestamps: list[tuple[float, dict]] = []
    with client.stream("POST", "/run", json={"code": code}, headers=HEADERS) as resp:
        assert resp.status_code == 200
        for line in resp.iter_lines():
            if line.strip():
                timestamps.append((time.monotonic(), json.loads(line)))

    stdout_chunks = [(t, m["text"]) for t, m in timestamps if m["type"] == "stdout"]
    first_t = next(t for t, txt in stdout_chunks if "Xin chào" in txt)
    second_t = next(t for t, txt in stdout_chunks if "Tạm biệt" in txt)
    assert second_t - first_t >= 0.4
    assert timestamps[-1][1] == {"type": "done", "ok": True, "error": None}


