Class `MessageLog` giữ một danh sách các tin nhắn chat. Nó phải hoạt động như sau:

- `add(text)` lưu một tin nhắn.
- `count()` trả về số tin nhắn đang lưu.
- `longest()` trả về nội dung tin nhắn dài nhất (lấy tin đầu tiên nếu có nhiều tin dài bằng nhau), hoặc `""` nếu log rỗng.

Đoạn code bên dưới có **3 lỗi**, và cả ba đều là quên `self`. Hãy chạy test, tìm và sửa chúng. Sửa code **bên trong class**; đừng đổi tên method.

**Ví dụ**

```python
log = MessageLog()
log.add("hi")
log.add("hello there")
print(log.count())     # 2
print(log.longest())   # hello there
```

**Quy tắc**
- Giữ nguyên tên class và tên các method.
- Mỗi object `MessageLog` giữ tin nhắn riêng của nó.
- Chỉ sửa ba lỗi `self`; method `longest` đã đúng rồi.
