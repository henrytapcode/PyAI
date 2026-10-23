Biến `Message` thành một dataclass cho ứng dụng chat. Một message có role, nội dung và một list tag, và nó biết đếm số từ của mình cũng như tự chuyển thành dict. Hãy viết code bên trong class và hai method, rồi `return` kết quả (đừng print).

**Ví dụ**

```python
msg = Message("user", "Hi there")
print(msg)                # Message(role='user', content='Hi there', tags=[])
print(msg.word_count())   # 2
print(msg.to_dict())      # {'role': 'user', 'content': 'Hi there', 'tags': []}
print(msg == Message("user", "Hi there"))   # True
```

**Quy tắc**
- `Message` có ba field theo thứ tự này: `role`, `content` và `tags`.
- `role` và `content` là bắt buộc. `tags` là tùy chọn và mặc định là list rỗng.
- Mỗi message có list `tags` **riêng**: thêm một tag vào message này không được làm đổi message khác.
- `word_count()` trả về số từ của `content` (các từ cách nhau bằng khoảng trắng). `content` rỗng có `0` từ.
- `to_dict()` trả về một dict với các key `"role"`, `"content"` và `"tags"`.
