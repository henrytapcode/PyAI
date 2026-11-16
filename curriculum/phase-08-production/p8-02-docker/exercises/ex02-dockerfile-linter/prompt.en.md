Write a Dockerfile text parser `parse_dockerfile(text)` and a static checker `lint(text)` using pure Python. Write your code inside both functions in `starter.py` and `return` the results.

**Example**

```python
parse_dockerfile("from python:3.13-slim\nRUN pip install \\\n  fastapi\n")
# [('FROM', 'python:3.13-slim'), ('RUN', 'pip install fastapi')]

lint("FROM python:latest\nCOPY . .\nRUN pip install -r requirements.txt\n")
# ['unpinned-base', 'copy-before-install']
```

**Rules**
- `parse_dockerfile(text)` returns `list[tuple[str, str]]`: uppercase instruction name and stripped arguments, skipping blank lines and `#` comments, and joining lines ending with `\` with a single space.
- `lint(text)` returns warning codes in this fixed order (at most once per code, or `[]` when clean):
  1. `"unpinned-base"`: a `FROM` image has no `:` tag or uses `:latest` (case-insensitive).
  2. `"copy-before-install"`: `COPY . .` appears before the first `RUN` instruction containing `pip install`.
  3. `"secret-in-image"`: `COPY` or `ADD` copies `.env` (not `.env.example`), or `ENV` defines a variable whose name contains `KEY`, `TOKEN`, or `SECRET`.
  4. `"localhost-cmd"`: `CMD` contains `127.0.0.1` or `localhost`.
