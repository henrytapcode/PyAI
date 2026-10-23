# Hàm phụ và list comprehension

Phiên bản này chuyển việc "một record thành một `Expense`" vào hàm riêng `record_to_expense`, hàm này cũng lo việc đổi `TypeError` thành `ValueError`. Khi đó `load_expenses` chỉ còn là một list comprehension. Phép kiểm tra ngày cũng được viết theo cách khác: so sánh list độ dài các phần với `[4, 2, 2]`, và nối các phần lại để thử `isdigit()` một lần. Trong `edit_expenses`, file không tồn tại được xử lý bằng cách bắt `FileNotFoundError` thay vì hỏi `exists()` trước.

Đây là lựa chọn tốt hơn khi cùng một phép chuyển đổi cần ở nhiều nơi, và các hàm nhỏ dễ test riêng. Nếu chỉ dùng một chỗ, vòng lặp với `try/except` ngay trong `load_expenses` cũng tốt không kém và giữ mọi thứ ở một nơi. Hỏi `exists()` trước (lời giải chính) đọc đơn giản hơn cho trường hợp thiếu file, nhưng bản `try/except` cũng bao được trường hợp file biến mất giữa hai bước.
