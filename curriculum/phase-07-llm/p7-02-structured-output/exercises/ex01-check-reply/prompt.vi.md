Hoàn thành hàm `check_reply(data, schema)` bằng cách thay các chỗ trống `___` trong `starter.py` để kiểm tra các khóa bắt buộc và kiểu dữ liệu theo một JSON schema tối giản.

Viết code bên trong hàm và `return` danh sách các chuỗi lỗi.

## Ví dụ

```python
schema = {
    "properties": {"name": {"type": "string"}, "order_id": {"type": "integer"}},
    "required": ["name", "order_id"],
}
check_reply({"name": "Lan", "order_id": True}, schema)
# -> ["wrong type: order_id"]
```

## Quy tắc

- Trả về `"missing: <key>"` cho mỗi khóa trong `schema.get("required", [])` bị thiếu khỏi `data`.
- Trả về `"wrong type: <key>"` cho mỗi khóa có mặt trong cả `data` và `schema.get("properties", {})` nhưng giá trị không khớp kiểu khai báo.
- Hỗ trợ bốn kiểu: `"string"`, `"integer"`, `"number"` và `"boolean"`.
- Từ chối giá trị `bool` (`True` / `False`) đối với `"integer"` và `"number"`.
- Chấp nhận cả `int` lẫn `float` (trừ `bool`) đối với `"number"`.
- Không báo lỗi nếu một khóa không nằm trong `"required"` bị bỏ qua trong `data`.
