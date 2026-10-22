"""Claude Code PostToolUse hook: after editing a file in curriculum/, validate that lesson.

Reads the hook JSON from stdin. Exit code 2 feeds the validator output back to Claude.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURRICULUM = ROOT / "curriculum"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0
    path = Path(file_path).resolve()
    if CURRICULUM not in path.parents:
        return 0
    # Find the lesson folder (the one holding meta.yaml), else validate the file's folder.
    target = next((p for p in [path.parent, *path.parents] if (p / "meta.yaml").exists()), path.parent)
    if CURRICULUM not in [target, *target.parents]:
        return 0
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate.py"), "--fast", "--allow-missing-vi", "--path", str(target)],
        capture_output=True, text=True, encoding="utf-8",
    )
    if proc.returncode != 0:
        print(proc.stdout[-4000:], file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
