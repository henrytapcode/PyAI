Hoàn thành `tool_schema(name, description, params, required)` trong `starter.py` bằng cách thay từng chỗ trống `___` để mô tả hàm Python thành tool schema hợp lệ.

Viết code bên trong hàm và `return` dictionary schema kết quả.

## Ví dụ

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

## Quy tắc

- Chỉ chấp nhận bốn kiểu JSON cơ bản: `"string"`, `"number"`, `"integer"` và `"boolean"`.
- Raise `ValueError` nếu có giá trị nào trong `params` không thuộc bốn kiểu trên.
- Raise `ValueError` nếu có tên nào trong `required` không nằm trong các key của `params`.
- Giữ nguyên thứ tự của `required` (tạo bản sao list mới) và ánh xạ từng cặp `p: t` trong `params` thành `p: {"type": t}` bên trong `parameters["properties"]`.
