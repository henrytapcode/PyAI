def check_reply(data: dict, schema: dict) -> list[str]:
    """Validate a parsed JSON dict against a minimal schema with enum support.

    Example:
        check_reply({"status": "pending"}, {"properties": {"status": {"enum": ["open", "closed"]}}})
        -> ["status: must be one of ['open', 'closed']"]
    """
    type_map = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
    }
    errors: list[str] = []
    for key in schema.get("required", []):
        if key not in data:
            errors.append(f"missing: {key}")

    for key, spec in schema.get("properties", {}).items():
        if key not in data:
            continue
        expected_type = spec.get(___, "")
        value = data[key]
        if expected_type in ("integer", "number") and isinstance(value, bool):
            errors.append(f"wrong type: {key}")
            continue
        expected = type_map.get(expected_type)
        if expected is not None and not isinstance(value, expected):
            errors.append(f"wrong type: {key}")
            continue
        # TODO: replace each ___ blank to check optional enum values in order
        allowed = spec.get(___)
        if allowed is not None and ___:
            errors.append(f"{key}: must be one of {___}")
    return errors
