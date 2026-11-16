# Simulate .dockerignore filtering on a RAG service project tree.

from fnmatch import fnmatch
from pathlib import PurePosixPath

PROJECT_FILES = [
    "main.py",
    "requirements.txt",
    "Dockerfile",
    "rag/retriever.py",
    ".env",
    ".env.example",
    ".venv/bin/python",
    ".git/HEAD",
    "__pycache__/main.cpython-313.pyc",
    "rag/__pycache__/retriever.cpython-313.pyc",
    "data/raw/handbook.pdf",
]

SAFE_DOCKERIGNORE = [
    ".venv/",
    ".git/",
    "__pycache__/",
    "*.pyc",
    ".env",
    "data/raw/",
]


def is_ignored(rel_path: str, patterns: list[str]) -> bool:
    """Simplified .dockerignore matcher using fnmatch and path parts."""
    path = PurePosixPath(rel_path)
    for raw in patterns:
        pat = raw.strip()
        if not pat or pat.startswith("#"):
            continue
        if pat.endswith("/"):
            folder = pat.rstrip("/")
            if rel_path.startswith(folder + "/") or folder in path.parts[:-1]:
                return True
        elif fnmatch(rel_path, pat) or fnmatch(path.name, pat):
            return True
    return False


def audit_context(files: list[str], patterns: list[str]) -> tuple[list[str], list[str]]:
    included: list[str] = []
    excluded: list[str] = []
    for path in files:
        if is_ignored(path, patterns):
            excluded.append(path)
        else:
            included.append(path)
    return included, excluded


kept, dropped = audit_context(PROJECT_FILES, SAFE_DOCKERIGNORE)
print("Sent to build context:")
for f in kept:
    print(f"  + {f}")

print("\nExcluded by .dockerignore:")
for f in dropped:
    print(f"  - {f}")

leaky_patterns = [p for p in SAFE_DOCKERIGNORE if p != ".env"]
for label, pats in [("Safe .dockerignore", SAFE_DOCKERIGNORE), ("Missing .env rule", leaky_patterns)]:
    ctx, _ = audit_context(PROJECT_FILES, pats)
    if ".env" in ctx:
        print(f"\n[{label}] WARNING: .env leaked into build context!")
    else:
        print(f"\n[{label}] OK: .env is excluded from build context.")
