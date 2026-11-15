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
    # TODO: replace each ___ blank to validate types, required names, and build schema
    for param_type in params.values():
        if ___:
            raise ValueError(f"unsupported type: {param_type}")
    for req in required:
        if ___:
            raise ValueError(f"unknown required parameter: {req}")
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": ___,
            "required": ___,
        },
    }
