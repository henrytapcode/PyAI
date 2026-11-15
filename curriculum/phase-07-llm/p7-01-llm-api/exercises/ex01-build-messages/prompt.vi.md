Hãy điền vào các chỗ trống `___` trong hàm `build_messages(system, history, user)` để trả về danh sách đầy đủ các dictionary message sẵn sàng gửi cho `FakeLLM().chat(...)`.

Mỗi phần tử trong `history` là một tuple `(user_text, assistant_text)` đại diện cho một lượt hỏi đáp trước đó. Hãy viết code bên trong hàm và `return` danh sách kết quả.

**Ví dụ**

```python
build_messages("Be concise.", [("Hi", "Hello!")], "What is RAG?")
# [
#     {"role": "system", "content": "Be concise."},
#     {"role": "user", "content": "Hi"},
#     {"role": "assistant", "content": "Hello!"},
#     {"role": "user", "content": "What is RAG?"},
# ]
```

**Quy tắc**

- Bắt đầu bằng một message `"system"`, tiếp theo là từng cặp `(user, assistant)` trong `history` thành hai message, và kết thúc bằng message `"user"` mới.
- Chạy đúng ngay cả khi `history` rỗng (`[]`).
- Không sửa đổi trực tiếp `history` tại chỗ.
