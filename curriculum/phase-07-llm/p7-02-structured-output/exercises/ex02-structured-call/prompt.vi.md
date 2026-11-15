Hãy viết hai hàm `parse_reply(text)` và `get_ticket(client, messages, schema, max_attempts=3)` để trích xuất JSON từ phản hồi lẫn tạp chất và retry kèm thông báo lỗi trước khi fallback về `None`.

Viết code bên trong các hàm trong `starter.py` (dùng hàm `_check_reply` có sẵn) và `return` kết quả theo đúng yêu cầu.

## Ví dụ

```python
parse_reply('Sure!\n```json\n{"name": "Lan", "order_id": 1042}\n```')
# -> {"name": "Lan", "order_id": 1042}

client = FakeLLM(script=['{"name": "Lan"}', '{"name": "Lan", "order_id": 1042}'])
get_ticket(client, [{"role": "user", "content": "ticket"}], schema, max_attempts=3)
# -> ({"name": "Lan", "order_id": 1042}, 2)
```

## Quy tắc

- `parse_reply(text)` cắt từ dấu `"{"` đầu tiên tới dấu `"}"` cuối cùng rồi parse bằng `json.loads()`.
- `parse_reply(text)` phải `raise ValueError` nếu thiếu `"{"` hoặc `"}"`, giải mã JSON thất bại, hoặc kết quả không phải `dict`.
- `get_ticket(client, messages, schema, max_attempts=3)` gọi `client.chat(..., response_format={"type": "json", "schema": schema})`, parse bằng `parse_reply` và kiểm tra bằng `_check_reply`.
- Nếu `parse_reply` ném `ValueError` hoặc `_check_reply` trả danh sách lỗi không rỗng, nối thêm một tin nhắn `"assistant"` chứa phản hồi hỏng và một tin nhắn `"user"` nêu lỗi, rồi thử lại.
- Trả về `(data, attempt)` ngay khi nhận được kết quả hợp lệ, hoặc `(None, max_attempts)` nếu hết lượt vẫn lỗi.
- Không được sửa trực tiếp danh sách `messages` gốc của người gọi.
