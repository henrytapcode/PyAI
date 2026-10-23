from pathlib import Path


def read_clean_lines(path):
    text = Path(path).read_text(encoding="utf-8")
    lines = []
    for line in text.splitlines():
        clean = line.strip()
        if clean:
            lines.append(clean)
    return lines
