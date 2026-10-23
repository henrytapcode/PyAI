Các dịch vụ AI thỉnh thoảng bị lỗi: hết thời gian chờ, máy chủ bận. Thường cách tốt nhất là cứ thử lại. Hãy viết `retry(times)`, một decorator có tham số. Hàm được decorate bằng `@retry(3)` sẽ được gọi tối đa 3 lần cho đến khi có một lần chạy được. Hãy viết code bên trong hàm và `return` decorator.

**Ví dụ**

```python
@retry(3)
def ask_llm(prompt):
    ...   # raises an error on the first two calls, returns "ok" on the third
```

| điều xảy ra bên trong | `ask_llm("hi")` |
|---|---|
| lần 1 raise, lần 2 raise, lần 3 trả về `"ok"` | trả về `"ok"` |
| cả 3 lần đều raise (lỗi cuối ghi `boom 3`) | raise lỗi ghi `boom 3` |

**Quy tắc**
- `times` ít nhất là 1 và là **tổng** số lần thử, nên lần thử đầu cũng được tính.
- Trả về kết quả của lần gọi đầu tiên chạy được rồi dừng. Đừng gọi hàm thêm lần nữa.
- Mọi `Exception` đều tính là thất bại và được thử lại. Nếu lần thử cuối cũng thất bại, raise lỗi của lần thử cuối đó.
- Bài về exception khuyên tránh `except Exception:` trống trơn. Wrapper retry là một trong số ít chỗ hợp lý để dùng nó, vì cuối cùng nó raise lại lỗi. Code thật thường chỉ thử lại với những lỗi cụ thể, ví dụ `TimeoutError`.
- Chuyển tiếp mọi đối số vị trí và đối số từ khóa cho hàm gốc.
- Hàm được decorate giữ nguyên tên và docstring gốc.
- Đừng chờ hay sleep giữa các lần thử.
