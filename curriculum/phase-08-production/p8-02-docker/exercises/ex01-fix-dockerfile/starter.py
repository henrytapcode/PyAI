# TODO: Fix the 4 bugs in DOCKERFILE so all checks pass:
#   1. Base image check fails (tag is not pinned to a concrete version)
#   2. Build cache check fails (editing app code forces dependencies to reinstall)
#   3. Image size check fails (pip keeps downloaded wheel archives in the layer)
#   4. Host connectivity check fails (container refuses traffic forwarded from host)

DOCKERFILE = """
FROM python:latest
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
""".strip()
