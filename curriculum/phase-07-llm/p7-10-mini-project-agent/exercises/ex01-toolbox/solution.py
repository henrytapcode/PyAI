import copy
import json


class ToolBox:
    """Allowlisted registry and validator for agent tool functions."""

    def __init__(self) -> None:
        """Initialize separate ordered containers for tools, schemas, and flags."""
        self._order: list[str] = []
        self._funcs: dict = {}
        self._schemas: dict[str, dict] = {}
        self._side_effects: dict[str, bool] = {}

    def register(self, fn, schema: dict, side_effect: bool = False) -> None:
        """Register a tool callable with its schema and side-effect flag."""
        tool_name = schema["name"]
        if tool_name in self._funcs:
            raise ValueError(f"duplicate tool: {tool_name}")
        self._order.append(tool_name)
        self._funcs[tool_name] = fn
        self._schemas[tool_name] = copy.deepcopy(schema)
        self._side_effects[tool_name] = bool(side_effect)

    def schemas(self) -> list[dict]:
        """Return deep copies of registered schemas in registration order."""
        return [copy.deepcopy(self._schemas[name]) for name in self._order]

    def is_side_effect(self, name: str) -> bool:
        """Return whether a registered tool has side effects (False if unknown)."""
        return self._side_effects.get(name, False)

    def call(self, name: str, args: dict) -> str:
        """Validate args, invoke tool inside try/except, and return string output."""
        if name not in self._funcs:
            return f"error: unknown tool {name}"
        params = self._schemas[name].get("parameters", {})
        for req_key in params.get("required", []):
            if req_key not in args or args[req_key] is None or args[req_key] == "":
                return f"error: missing {req_key}"
        allowed_props = params.get("properties", {})
        filtered_args = {k: v for k, v in args.items() if k in allowed_props}
        try:
            outcome = self._funcs[name](**filtered_args)
        except Exception as exc:
            return f"error: {exc}"
        if isinstance(outcome, (dict, list)):
            return json.dumps(outcome)
        return str(outcome)
