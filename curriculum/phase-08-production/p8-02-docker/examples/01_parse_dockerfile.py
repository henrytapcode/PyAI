# Parse a Dockerfile with comments, blank lines, and line continuations.

DOCKERFILE = """
# Base Python runtime
FROM python:3.13-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir \\
    -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""


def parse_dockerfile(text: str) -> list[tuple[str, str]]:
    """Return (INSTRUCTION, args) pairs, skipping comments and joining \\ lines."""
    parsed: list[tuple[str, str]] = []
    pending = ""
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith("\\"):
            pending += line[:-1].rstrip() + " "
            continue
        full = (pending + line).strip()
        pending = ""
        parts = full.split(None, 1)
        inst = parts[0].upper()
        args = parts[1].strip() if len(parts) > 1 else ""
        parsed.append((inst, args))
    return parsed


instructions = parse_dockerfile(DOCKERFILE)
print(f"{'INSTRUCTION':<11} | ARGS")
print("-" * 45)
for inst, args in instructions:
    print(f"{inst:<11} | {args}")

layer_ops = {"RUN", "COPY", "ADD"}
layer_count = sum(1 for inst, _ in instructions if inst in layer_ops)
print(f"\nTotal instructions: {len(instructions)}")
print(f"Filesystem layers (RUN/COPY/ADD): {layer_count}")
