Giờ là nửa báo cáo của expense tracker. Với một list các object `Expense`, hãy cộng chúng theo danh mục và theo tháng, rồi tìm danh mục tiêu nhiều tiền nhất. `Expense` đã được viết sẵn trong editor. Hãy viết code bên trong ba hàm và `return` kết quả. Phần 7 của bài học có vòng lặp accumulator và phép slice lấy tháng.

**Ví dụ**

```python
expenses = [
    Expense("2024-01-05", "food", 4.5),
    Expense("2024-01-09", "fun", 9.0),
    Expense("2024-02-01", "food", 6.25),
]
totals_by_category(expenses)   # {"food": 10.75, "fun": 9.0}
totals_by_month(expenses)      # {"2024-01": 13.5, "2024-02": 6.25}
top_category(expenses)         # "food"
```

**Quy tắc**

- `totals_by_category(expenses)` trả về một dict ánh xạ mỗi danh mục tới tổng số tiền của nó. Các key theo thứ tự bảng chữ cái, và mỗi tổng được làm tròn 2 chữ số thập phân bằng `round(total, 2)`.
- `totals_by_month(expenses)` làm tương tự cho các tháng. Key là 7 ký tự đầu của ngày (`"2024-01"`), và các key theo thứ tự từ tháng cũ nhất đến mới nhất. Các tổng được làm tròn 2 chữ số thập phân. Cùng một tháng của hai năm khác nhau cho hai key khác nhau.
- `top_category(expenses)` trả về **tên** danh mục có tổng lớn nhất (so sánh các tổng đã làm tròn từ `totals_by_category`). Nếu hai danh mục có cùng tổng lớn nhất, trả về danh mục đứng trước trong bảng chữ cái. Với list rỗng trả về `None`.
- List rỗng cho `{}` ở hai hàm tính tổng.
- Mọi số tiền đều lớn hơn `0` (chúng đã qua `check_expense`), nên bạn không cần kiểm tra lại.
- Không thay đổi list bạn nhận vào.

Bấm **Kiểm tra** để chạy test.
