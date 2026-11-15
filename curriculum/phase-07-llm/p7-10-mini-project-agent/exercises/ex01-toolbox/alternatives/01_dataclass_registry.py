import copy
import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class _ToolEntry:
    fn: Callable[..., Any]
    schema: dict
    side_effect: bool


class ToolBox:
    """Allowlisted toolbox backed by a single dict of frozen _ToolEntry records."""

    def __init__(self) -> None:
        self._entries: dict[str, _ToolEntry] = {}

    def register(self, fn, schema: dict, side_effect: bool = False) -> None:
        name = schema["name"]
        if name in self._entries:
            raise ValueError(f"duplicate tool: {name}")
        self._entries[name] = _ToolEntry(
            fn=fn,
            schema=copy.deepcopy(schema),
            side_effect=bool(side_effect),
        )

    def schemas(self) -> list[dict]:
        return [copy.deepcopy(entry.schema) for entry in self._entries.values()]

    def is_side_effect(self, name: str) -> bool:
        entry = self._entries.get(name)
        return entry.side_effect if entry is not None else False

    def _prepare_args(self, schema: dict, args: dict) -> tuple[dict | None, str | None]:
        params = schema.get("parameters", {})
        for req in params.get("required", []):
            val = args.get(req)
            if req not in args or val is None or val == "":
                return None, f"error: missing {req}"
        props = params.get("properties", {})
        return {k: v for k, v in args.items() if k in props}, None

    def call(self, name: str, args: dict) -> str:
        entry = self._entries.get(name)
        if entry is None:
            return f"error: unknown tool {name}"
        clean, err = self._prepare_args(entry.schema, args)
        if err is not None:
            return err
        try:
            res = entry.fn(**clean)
        except Exception as exc:
            return f"error: {exc}"
        return json.dumps(res) if isinstance(res, (dict, list)) else str(res)
