def check_reply(data: dict, schema: dict) -> list[str]:
    """Validate a parsed JSON dict against a minimal schema.

    Example: check_reply({"name": "Lan"}, {"required": ["name"]}) -> []
    """
    type_map = {
        "string": str,
        "integer": int,
        "number": (int, float),
        "boolean": bool,
    }
    errors: list[str] = []
    # TODO: replace each ___ blank to check required keys and property types
    for key in schema.get("required", []):
        if ___:
            errors.append(f"missing: {key}")

    for key, spec in schema.get("properties", {}).items():
        if key not in data:
            continue
        expected_type = spec.get("type", "")
        value = data[key]
        if expected_type in ("integer", "number") and ___:
            errors.append(f"wrong type: {key}")
            continue
        expected = type_map.get(expected_type)
        if expected is not None and not ___:
            errors.append(f"wrong type: {key}")
    return errors
