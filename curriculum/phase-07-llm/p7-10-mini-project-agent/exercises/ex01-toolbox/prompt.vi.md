Cài đặt class `ToolBox` gồm các phương thức `register`, `schemas`, `is_side_effect` và `call` để quản lý bộ tool có allowlist cho agent. Viết code bên trong các phương thức của class và `return` kết quả đúng quy định.

**Ví dụ**

```python
box = ToolBox()
box.register(
    lambda order_id: {"id": order_id, "status": "delayed"},
    {
        "name": "lookup_order",
        "description": "Look up an order",
        "parameters": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}},
            "required": ["order_id"],
        },
    },
    side_effect=False,
)
print(box.is_side_effect("lookup_order"))            # False
print(box.call("lookup_order", {"order_id": "1042"}))  # {"id": "1042", "status": "delayed"}
print(box.call("unknown", {}))                        # error: unknown tool unknown
```

**Quy tắc**

- `register(fn, schema: dict, side_effect: bool = False) -> None`:
  - Lấy tên tool từ `schema["name"]`.
  - Raise `ValueError` nếu tên tool này đã được đăng ký trước đó.
- `schemas() -> list[dict]`:
  - Trả về danh sách schema của các tool theo đúng thứ tự đăng ký.
  - Trả về bản sao sâu (deep copy) để việc chỉnh sửa list hoặc dict trả về không làm thay đổi trạng thái bên trong `ToolBox`.
- `is_side_effect(name: str) -> bool`:
  - Trả về `True` nếu `name` được đăng ký với `side_effect=True`, ngược lại trả về `False` (kể cả khi `name` chưa đăng ký).
- `call(name: str, args: dict) -> str`:
  - Nếu `name` chưa đăng ký, trả về `f"error: unknown tool {name}"`.
  - Kiểm tra `parameters.get("required", [])` theo đúng thứ tự; nếu khóa vắng mặt trong `args` hoặc có giá trị `None` hay `""`, trả về `f"error: missing {key}"` cho khóa thiếu đầu tiên.
  - Bỏ qua mọi khóa trong `args` không nằm trong `parameters.get("properties", {})`, và tuyệt đối không làm thay đổi dictionary `args` đầu vào.
  - Gọi hàm đã đăng ký với các tham số đã lọc trong `try/except`; nếu gặp bất kỳ `Exception as err` nào, trả về `f"error: {err}"`.
  - Chuyển kết quả kiểu `dict` và `list` bằng `json.dumps()`, còn mọi kiểu khác chuyển bằng `str()`.
