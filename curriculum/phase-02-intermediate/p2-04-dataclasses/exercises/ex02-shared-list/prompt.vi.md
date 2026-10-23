File dưới đây định nghĩa hai dataclass, nhưng có 3 lỗi. `Chat` giữ một list các đoạn tin nhắn, còn `GenerationConfig` chứa các cài đặt chỉ đọc cho một model. Hãy chạy code, đọc lỗi và sửa cho đến khi mọi test đều qua. Chỉ sửa phần định nghĩa class.

**Ví dụ**

```python
chat = Chat("demo")
chat.add("Hi")
print(chat.messages)     # ['Hi']
print(Chat("other").messages)   # []  (chat mới bắt đầu rỗng)

config = GenerationConfig("small", temperature=0.2)
print(config)            # GenerationConfig(model='small', temperature=0.2, max_tokens=256)
config.max_tokens = 1    # lỗi: config chỉ đọc
```

**Quy tắc**
- Một `Chat` mới bắt đầu với list `messages` rỗng, và **mỗi chat có list riêng**.
- `Chat.add(text)` và `Chat.count()` đã chạy đúng. Đừng sửa chúng.
- Cũng có thể đưa sẵn các message khi tạo chat: `Chat("demo", ["a", "b"])`.
- `GenerationConfig` có các field `model` (bắt buộc), `temperature` (mặc định `0.7`) và `max_tokens` (mặc định `256`), theo thứ tự này.
- Một `GenerationConfig` không thể bị đổi sau khi tạo: gán vào bất kỳ field nào cũng gây lỗi.
