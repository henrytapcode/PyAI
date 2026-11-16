def parse_dockerfile(text: str) -> list[tuple[str, str]] | None:
    """Parse a Dockerfile into uppercase (INSTRUCTION, args) tuples.

    Example:
        parse_dockerfile("# base\\nfrom python:3.13-slim\\nRUN pip install \\\\\\n  fastapi")
        -> [("FROM", "python:3.13-slim"), ("RUN", "pip install fastapi")]
    """
    # TODO: skip blank lines and # comments, join trailing \ continuations,
    #       uppercase each instruction, and strip its arguments
    return None


def lint(text: str) -> list[str] | None:
    """Return Dockerfile lint warning codes in fixed order.

    Order: unpinned-base, copy-before-install, secret-in-image, localhost-cmd.

    Example:
        lint("FROM python:latest\\nCMD uvicorn main:app --host 127.0.0.1")
        -> ["unpinned-base", "localhost-cmd"]
    """
    # TODO: call parse_dockerfile(text) and check the four lint rules in order
    return None
