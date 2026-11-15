ALLOWED_TYPES = {"string", "number", "integer", "boolean"}


def tool_schema(
    name: str,
    description: str,
    params: dict[str, str],
    required: list[str],
) -> dict:
    """Build and validate a tool schema dict for LLM tool calling.

    Example: tool_schema("get_weather", "weather city", {"city": "string"}, ["city"])
    """
    for param_type in params.values():
        if param_type not in ALLOWED_TYPES:
            raise ValueError(f"unsupported type: {param_type}")
    for req in required:
        if req not in params:
            raise ValueError(f"unknown required parameter: {req}")
    deduped_required = list(dict.fromkeys(required))
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": {p: {"type": t} for p, t in params.items()},
            "required": deduped_required,
        },
    }
