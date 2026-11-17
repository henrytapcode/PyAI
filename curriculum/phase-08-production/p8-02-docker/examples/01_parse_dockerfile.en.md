# Parse a Dockerfile into instructions and layers

**What it shows:** Splitting a realistic `Dockerfile` string into normalized `(INSTRUCTION, args)` tuples while ignoring comments, blank lines, and `\` line continuations, then counting filesystem layers.

**Step by step**
1. Lines 3–14 define `DOCKERFILE` with a `#` comment, a blank line, and a multi-line `RUN pip install ...` joined with `\`.
2. Lines 17–34 implement `parse_dockerfile(text)` by stripping each line, skipping empty/comment lines, accumulating `\` continuations in `pending`, and splitting once on whitespace into `(INSTRUCTION, args)`.
3. Lines 37–46 print a formatted `INSTRUCTION | ARGS` table and count how many instructions (`RUN`, `COPY`, `ADD`) add filesystem layers.

**Notice:** `parse_dockerfile` normalizes `RUN pip install --no-cache-dir \` and `-r requirements.txt` into a single `RUN` entry, so downstream tools see one instruction rather than two broken lines.

**Try it yourself:** Add `ENV PYTHONUNBUFFERED=1` after `WORKDIR /app` and verify that total instructions rise from `7` to `8` while filesystem layers (`RUN`/`COPY`/`ADD`) stay at `3`.
