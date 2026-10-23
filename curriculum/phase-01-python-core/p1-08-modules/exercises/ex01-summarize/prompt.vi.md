Sau mỗi thí nghiệm, bạn báo cáo vài con số về điểm của mình. Thư viện chuẩn đã có sẵn công cụ, nên hãy import chúng thay vì tự viết công thức. Hãy viết hai hàm trong file và `return` kết quả.

1. `summarize(values)` nhận một list có ít nhất hai số và trả về dict với các key `"count"`, `"mean"`, `"median"` và `"stdev"`. Làm tròn `"stdev"` đến 2 chữ số thập phân; các giá trị còn lại để nguyên.
2. `same_average(a, b)` nhận hai list số và trả về `True` nếu trung bình của chúng bằng nhau trên thực tế, ngược lại trả về `False`.

**Ví dụ**

| Lời gọi | Kết quả |
|---|---|
| `summarize([70, 80, 90, 100])` | `{"count": 4, "mean": 85, "median": 85.0, "stdev": 12.91}` |
| `same_average([0.1, 0.2], [0.15])` | `True` |
| `same_average([1, 2, 3], [5])` | `False` |

**Quy tắc**
- Dùng `statistics` cho phần tóm tắt và `math.isclose` để so sánh các giá trị trung bình.
- Đặt các dòng `import` ở đầu file.
- `return` giá trị, đừng `print`.
