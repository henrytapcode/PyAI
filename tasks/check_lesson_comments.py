"""Run every ```python block in lesson.*.md files and compare `# ...` output comments.

Rule: comment lines that come right after a line containing `print(` (consecutive lines
starting with `# `) are expected stdout lines. Every expected line must appear in the
block's real stdout, in order. Usage:
    uv run python tasks/check_lesson_comments.py <lesson dir> [<lesson dir> ...]
"""

import re
import subprocess
import sys
from pathlib import Path

FENCE = re.compile(r"```python\n(.*?)```", re.S)


def expected_lines(code: str) -> list[str]:
    out: list[str] = []
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if "print(" not in line or line.lstrip().startswith("#"):
            continue
        j = i + 1
        while j < len(lines) and lines[j].startswith("# "):
            out.append(lines[j][2:])
            j += 1
    return out


def check(md: Path) -> int:
    bad = 0
    for n, m in enumerate(FENCE.finditer(md.read_text(encoding="utf-8")), 1):
        code = m.group(1)
        exp = expected_lines(code)
        if not exp:
            continue
        r = subprocess.run(
            [sys.executable, "-W", "error", "-c", code],
            capture_output=True, text=True, encoding="utf-8", timeout=60,
        )
        real = [ln.rstrip() for ln in r.stdout.splitlines()]
        exp = [e.rstrip() for e in exp]
        pos = 0
        for e in exp:
            try:
                pos = real.index(e, pos) + 1
            except ValueError:
                bad += 1
                print(f"{md} block {n}: expected line not in stdout: {e!r}")
                break
        if r.returncode != 0 or r.stderr.strip():
            bad += 1
            print(f"{md} block {n}: exit {r.returncode}, stderr: {r.stderr.strip()[:300]}")
    return bad


def main() -> None:
    total = 0
    for d in sys.argv[1:]:
        for md in sorted(Path(d).glob("lesson.*.md")):
            total += check(md)
    print("comment mismatches:", total)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
