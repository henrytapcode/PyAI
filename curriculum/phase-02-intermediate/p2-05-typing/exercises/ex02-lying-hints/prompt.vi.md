Bốn hàm dưới đây đều có type hint, và mỗi hint phải mô tả đúng sự thật về hàm. Chúng đang có lỗi: ở ba hàm thì **hint** sai, còn ở một hàm thì **code** sai. Hãy chạy test, tìm xem hàm nào lỗi ở đâu, rồi sửa. Docstring mô tả hành vi đúng.

**Ví dụ**

```python
average_length(["ab", "abcd"])   # 3.0   (một float, không phải int)
find_system([])                  # None  (không tìm thấy gì)
repeat("ab", 2)                  # "abab"
shout("hi")                      # "HI"
```

**Quy tắc**
- Giữ nguyên tên hàm và tên tham số.
- Sửa hint khi code đúng mà hint nói dối. Sửa code khi code không làm đúng như docstring mô tả.
- Đừng đổi giá trị `find_system` trả về khi không có message system: nó vẫn phải là `None`.
- Test kiểm tra cả kết quả lẫn hint: chúng đọc `__annotations__` giống cách một type checker làm.
