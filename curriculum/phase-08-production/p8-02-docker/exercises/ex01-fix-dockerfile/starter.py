# TODO: Fix the four bugs in DOCKERFILE:
#   1. Pin a specific Python tag instead of :latest
#   2. Copy requirements.txt and run pip install BEFORE COPY . .
#   3. Add --no-cache-dir to pip install
#   4. Bind 0.0.0.0 instead of 127.0.0.1 in CMD

DOCKERFILE = """
FROM python:latest
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
""".strip()
