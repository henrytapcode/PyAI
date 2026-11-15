class ToolBox:
    """Allowlisted registry and validator for agent tool functions."""

    def __init__(self) -> None:
        """Initialize an empty toolbox."""
        # TODO: set up internal storage for registered tools.
        pass

    def register(self, fn, schema: dict, side_effect: bool = False) -> None:
        """Register a tool callable with its JSON schema and side-effect flag.

        Example:
            box.register(fn, {"name": "ping", "parameters": {"properties": {}}}, False)
        """
        # TODO: read schema["name"], reject duplicates with ValueError, and store entry.
        pass

    def schemas(self) -> list[dict]:
        """Return deep copies of registered schemas in registration order."""
        # TODO: return copied schema dicts without exposing internal objects.
        return None

    def is_side_effect(self, name: str) -> bool:
        """Return True if name is registered with side_effect=True, else False."""
        # TODO: look up side-effect flag for name (False if unknown).
        return None

    def call(self, name: str, args: dict) -> str:
        """Validate args against schema, execute tool, and format output as str."""
        # TODO: handle unknown tools, missing required args, extra args, errors, and JSON output.
        return None
