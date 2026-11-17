import pytest

import exercise


def test_parse_skips_comments_and_blank_lines():
    raw = """
    # base runtime
    FROM python:3.13-slim

      # working dir
    WORKDIR   /app
    """
    assert exercise.parse_dockerfile(raw) == [
        ("FROM", "python:3.13-slim"),
        ("WORKDIR", "/app"),
    ]


def test_parse_joins_backslash_continuations():
    raw = """
    FROM python:3.13-slim
    RUN pip install --no-cache-dir \\
        -r requirements.txt
    """
    assert exercise.parse_dockerfile(raw) == [
        ("FROM", "python:3.13-slim"),
        ("RUN", "pip install --no-cache-dir -r requirements.txt"),
    ]


def test_parse_uppercases_lowercase_instructions():
    raw = "from python:3.13-slim\nworkdir /app\n"
    assert exercise.parse_dockerfile(raw) == [
        ("FROM", "python:3.13-slim"),
        ("WORKDIR", "/app"),
    ]


def test_lint_returns_empty_list_for_clean_dockerfile():
    clean = """
    # Clean FastAPI Dockerfile
    from python:3.13-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir \\
        -r requirements.txt
    COPY . .
    COPY .env.example .
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    """
    assert exercise.lint(clean) == []


@pytest.mark.parametrize(
    "snippet,expected_code",
    [
        (
            'FROM python\nCMD ["uvicorn", "main:app", "--host", "0.0.0.0"]',
            "unpinned-base",
        ),
        (
            'FROM python:latest\nCMD ["uvicorn", "main:app", "--host", "0.0.0.0"]',
            "unpinned-base",
        ),
        (
            'FROM python:LATEST\nCMD ["uvicorn", "main:app", "--host", "0.0.0.0"]',
            "unpinned-base",
        ),
        (
            "FROM python:3.13-slim\nCOPY . .\nRUN pip install -r requirements.txt",
            "copy-before-install",
        ),
        (
            "FROM python:3.13-slim\nRUN apt-get update\n"
            "COPY . .\nRUN pip install -r requirements.txt",
            "copy-before-install",
        ),
        ("FROM python:3.13-slim\nCOPY .env .", "secret-in-image"),
        ("FROM python:3.13-slim\nADD .env /app/.env", "secret-in-image"),
        ("FROM python:3.13-slim\nENV OPENAI_API_KEY=sk-test", "secret-in-image"),
        ("FROM python:3.13-slim\nENV HF_TOKEN=abc", "secret-in-image"),
        ("FROM python:3.13-slim\nENV DB_SECRET=x", "secret-in-image"),
        ("FROM python:3.13-slim\nENV MODE=prod API_KEY=abc", "secret-in-image"),
        (
            'FROM python:3.13-slim\nCMD ["uvicorn", "main:app", "--host", "127.0.0.1"]',
            "localhost-cmd",
        ),
        ("FROM python:3.13-slim\nCMD uvicorn main:app --host localhost", "localhost-cmd"),
    ],
)
def test_lint_detects_each_rule(snippet, expected_code):
    codes = exercise.lint(snippet)
    assert codes == [expected_code], f"expected [{expected_code!r}] for:\n{snippet}"


def test_lint_reports_all_errors_in_fixed_order():
    buggy = """
    FROM python:latest
    WORKDIR /app
    COPY . .
    COPY .env .
    RUN pip install -r requirements.txt
    CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
    """
    assert exercise.lint(buggy) == [
        "unpinned-base",
        "copy-before-install",
        "secret-in-image",
        "localhost-cmd",
    ]


def test_lint_handles_multiline_pip_install_after_copy_all():
    buggy = """
    # lowercase + backslash continuation
    from python:3.13-slim
    COPY . .
    RUN pip install \\
        --no-cache-dir -r requirements.txt
    """
    assert exercise.lint(buggy) == ["copy-before-install"]
