# Hàm phụ trả về `None`

Phần `try/except` được chuyển vào một hàm nhỏ, `parse_score`, hàm này trả về số hoặc `None` sau khi ghi warning. Vòng lặp chính chỉ giữ những kết quả không phải `None`. Hãy viết `is not None` thay vì `if score:` đơn thuần, vì điểm `0` là một số hợp lệ mà `if` đơn thuần sẽ vứt đi. Cách này dễ đọc hơn khi quy tắc phân tích dài ra (ví dụ "chấp nhận cả `7/10`"). Với quy tắc chỉ ba dòng thì lời giải đầu tiên ngắn hơn.
