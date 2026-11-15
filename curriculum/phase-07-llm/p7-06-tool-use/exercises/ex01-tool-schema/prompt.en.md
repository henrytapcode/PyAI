Complete `tool_schema(name, description, params, required)` in `starter.py` by replacing every `___` blank so Python functions can be described as valid tool schemas.

Write your code inside the function and `return` the schema dictionary.

## Example

```python
tool_schema(
    "get_weather",
    "weather city temperature",
    {"city": "string", "unit": "string"},
    ["city"],
)
# -> {
#     "name": "get_weather",
#     "description": "weather city temperature",
#     "parameters": {
#         "type": "object",
#         "properties": {"city": {"type": "string"}, "unit": {"type": "string"}},
#         "required": ["city"],
#     },
# }
```

## Rules

- Allowed JSON parameter types are the four basic types: `"string"`, `"number"`, `"integer"`, and `"boolean"`.
- Raise `ValueError` if any value in `params` is not one of the four allowed types.
- Raise `ValueError` if any name in `required` is not a key in `params`.
- Keep the first-seen order of `required` while removing any duplicate names (as a new list copy); `parameters["properties"]` is already built from `params`.
