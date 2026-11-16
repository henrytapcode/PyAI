The `DOCKERFILE` string in `starter.py` builds a FastAPI service image, but it contains four common mistakes: an unpinned base image, slow layer caching, cached `.whl` bloat in `pip install`, and a `127.0.0.1` host binding that blocks requests from outside the container. Fix `DOCKERFILE` directly so all four checks pass.

**Example**

```text
FROM python:3.13-slim
...
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
...
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Rules**
- Keep `DOCKERFILE` as a multi-line string inside `starter.py` (do not run `docker`).
- Pin `FROM` to a specific Python tag (not `latest` or untagged).
- Put `COPY requirements.txt .` before `RUN pip install`, and put `RUN pip install` before `COPY . .`.
- Pass `--no-cache-dir` to `pip install`.
- Keep `CMD` in JSON exec form (`[...]`) and bind `--host 0.0.0.0`.
