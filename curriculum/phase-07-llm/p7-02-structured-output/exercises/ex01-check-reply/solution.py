_TYPE_MAP: dict[str, type | tuple[type, ...]] = {
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
}


def _check_property(key: str, value: object, spec: dict) -> str | None:
    expected_type = spec.get("type", "")
    if expected_type in ("integer", "number") and isinstance(value, bool):
        return f"wrong type: {key}"
    expected = _TYPE_MAP.get(expected_type)
    if expected is not None and not isinstance(value, expected):
        return f"wrong type: {key}"
    allowed = spec.get("enum")
    if allowed is not None and value not in allowed:
        return f"{key}: must be one of {allowed}"
    return None


def check_reply(data: dict, schema: dict) -> list[str]:
    """Validate a parsed JSON dict against a minimal schema with enum support.

    Example:
        check_reply({"status": "pending"}, {"properties": {"status": {"enum": ["open", "closed"]}}})
        -> ["status: must be one of ['open', 'closed']"]
    """
    errors = [f"missing: {key}" for key in schema.get("required", []) if key not in data]
    for key, spec in schema.get("properties", {}).items():
        if key in data:
            err = _check_property(key, data[key], spec)
            if err is not None:
                errors.append(err)
    return errors
