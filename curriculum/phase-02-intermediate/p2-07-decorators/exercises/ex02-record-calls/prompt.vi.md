Decorator `record_calls` phải ghi mỗi lần gọi vào list `CALL_LOG` rồi cư xử y hệt hàm gốc. Nhưng các hàm được decorate bằng nó lại trả về sai. Hãy chạy test, tìm các bug, và sửa `record_calls` trong code khởi đầu.

**Ví dụ**

```python
@record_calls
def add(a, b=0):
    """Add two numbers."""
    return a + b

add(2, 3)      # returns 5, and CALL_LOG is now [("add", (2, 3))]
add(2, b=3)    # returns 5, and CALL_LOG gets ("add", (2,))
```

**Quy tắc**
- Mỗi lần gọi thêm một tuple `(tên hàm, các đối số vị trí)` vào `CALL_LOG`. Đối số từ khóa không nằm trong tuple.
- Hàm được decorate trả về đúng thứ hàm gốc trả về, với mọi đối số được chuyển tiếp.
- Hàm được decorate giữ nguyên tên và docstring gốc.
- Giữ nguyên tên `CALL_LOG` và khung của `record_calls`. Chỉ sửa các bug.
