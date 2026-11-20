"""Find runs of consecutive solution lines copied verbatim from lesson code blocks.

Usage: uv run python tasks/check_overlap.py <lesson dir> [min_run=5]
For every exercise solution.py, prints the share of code lines found anywhere in the
lesson's python blocks, and every run of >= min_run consecutive copied lines.
Lines compared stripped; blank lines, comments, imports and docstring-only lines skipped.
"""

import re
import sys
from pathlib import Path

FENCE = re.compile(r"```python\n(.*?)```", re.S)


def code_lines(text: str) -> list[str]:
    out = []
    for raw in text.splitlines():
        s = raw.strip()
        if not s or s.startswith("#") or s.startswith(("import ", "from ")):
            continue
        if s.startswith(('"""', "'''")):
            continue
        out.append(s)
    return out


def main() -> None:
    lesson = Path(sys.argv[1])
    min_run = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    lesson_text = (lesson / "lesson.en.md").read_text(encoding="utf-8")
    lesson_set = set()
    for m in FENCE.finditer(lesson_text):
        lesson_set.update(code_lines(m.group(1)))
    worst = 0
    for sol in sorted(lesson.glob("exercises/*/solution.py")):
        lines = code_lines(sol.read_text(encoding="utf-8"))
        hit = [ln in lesson_set for ln in lines]
        runs, cur, start = [], 0, 0
        for i, h in enumerate(hit + [False]):
            if h:
                if cur == 0:
                    start = i
                cur += 1
            else:
                if cur >= min_run:
                    runs.append((start, cur))
                cur = 0
        share = sum(hit) / max(len(lines), 1)
        print(f"{sol.parent.name}: {sum(hit)}/{len(lines)} lines in lesson ({share:.0%}), runs>={min_run}: {len(runs)}")
        for s, n in runs:
            print(f"   run of {n}: {lines[s]!r} .. {lines[s + n - 1]!r}")
            worst = max(worst, n)
    print("longest copied run:", worst)


if __name__ == "__main__":
    main()
