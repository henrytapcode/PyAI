import json

import exercise


def _parse(text: str) -> list[tuple[str, str]]:
    instructions: list[tuple[str, str]] = []
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
        instructions.append((parts[0].upper(), parts[1].strip() if len(parts) > 1 else ""))
    return instructions


def test_base_image_pins_a_specific_tag():
    rows = _parse(exercise.DOCKERFILE)
    froms = [args for inst, args in rows if inst == "FROM"]
    assert froms, "Dockerfile must start with a FROM instruction"
    image = froms[0].split()[0]
    assert ":" in image, f"pin a specific tag on {image!r} (e.g. python:3.13-slim)"
    tag = image.split(":")[-1].lower()
    assert tag and tag != "latest", "do not use :latest; pin an explicit version tag"


def test_copies_requirements_before_installing_then_app_code():
    rows = _parse(exercise.DOCKERFILE)
    copy_req_idx = next(
        (
            i
            for i, (inst, args) in enumerate(rows)
            if inst == "COPY" and "requirements.txt" in args.split()
        ),
        None,
    )
    pip_idx = next(
        (
            i
            for i, (inst, args) in enumerate(rows)
            if inst == "RUN" and "pip install" in " ".join(args.split())
        ),
        None,
    )
    copy_all_idx = next(
        (i for i, (inst, args) in enumerate(rows) if inst == "COPY" and args.split()[:1] == ["."]),
        None,
    )
    assert copy_req_idx is not None, "add COPY requirements.txt . before installing dependencies"
    assert pip_idx is not None, "add RUN pip install ... -r requirements.txt"
    assert copy_all_idx is not None, "keep COPY . . to copy the application code"
    assert copy_req_idx < pip_idx < copy_all_idx, (
        "layer order must be: COPY requirements.txt -> RUN pip install -> COPY . ."
    )


def test_pip_install_uses_no_cache_dir():
    rows = _parse(exercise.DOCKERFILE)
    pip_runs = [
        args
        for inst, args in rows
        if inst == "RUN" and "pip install" in " ".join(args.split())
    ]
    assert pip_runs, "expected a RUN pip install instruction"
    assert any("--no-cache-dir" in cmd for cmd in pip_runs), "pass --no-cache-dir to pip install"


def test_cmd_uses_exec_form_and_binds_all_interfaces():
    rows = _parse(exercise.DOCKERFILE)
    cmds = [args for inst, args in rows if inst == "CMD"]
    assert cmds, "Dockerfile must include a CMD instruction"
    raw_cmd = cmds[-1]
    assert raw_cmd.startswith("["), "CMD must use JSON exec form, e.g. CMD [\"uvicorn\", ...]"
    tokens = json.loads(raw_cmd)
    assert isinstance(tokens, list), "CMD exec form must be a JSON list of strings"
    assert "0.0.0.0" in tokens, "bind --host 0.0.0.0 so the host machine can reach the container"
    assert "127.0.0.1" not in tokens and "localhost" not in tokens, "remove loopback host from CMD"
