Hoàn thành hàm `check_reply(data, schema)` bằng cách thay các chỗ trống `___` trong `starter.py` để kiểm tra khóa bắt buộc, kiểu dữ liệu và giá trị `enum` cho phép theo một JSON schema tối giản.

Viết code bên trong hàm và `return` danh sách các chuỗi lỗi.

## Ví dụ

```python
schema = {
    "properties": {
        "name": {"type": "string"},
        "status": {"type": "string", "enum": ["open", "closed"]},
    },
    "required": ["name", "status"],
}
check_reply({"name": "Lan", "status": "pending"}, schema)
# -> ["status: must be one of ['open', 'closed']"]
```

## Quy tắc

- Trả về `"missing: <key>"` cho mỗi khóa trong `schema.get("required", [])` bị thiếu khỏi `data`.
- Trả về `"wrong type: <key>"` cho mỗi khóa có mặt trong cả `data` và `schema.get("properties", {})` nhưng giá trị không khớp kiểu khai báo.
- Hỗ trợ bốn kiểu `"string"`, `"integer"`, `"number"` và `"boolean"`, đồng thời từ chối giá trị `bool` (`True` / `False`) đối với `"integer"` và `"number"`.
- Nếu spec của một trường có `"enum"` và giá trị đã qua bước kiểm tra kiểu (nếu có) nhưng không nằm trong danh sách cho phép, nối thêm `f"{key}: must be one of {allowed}"` (ví dụ `"status: must be one of ['open', 'closed']"`).
- Thu thập lỗi `"missing: ..."` trước theo thứ tự `"required"`, rồi mới tới `"wrong type: ..."` hoặc `"<key>: must be one of ..."` theo thứ tự `"properties"`.
- Không báo lỗi nếu một khóa không nằm trong `"required"` bị bỏ qua trong `data`.
