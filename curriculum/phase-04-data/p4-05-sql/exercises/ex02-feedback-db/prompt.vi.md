Viết hai hàm để lưu và truy vấn đánh giá mô hình trong database SQLite bộ nhớ: `create_feedback_db(rows)` tạo bảng `feedback(user TEXT, model TEXT, rating INTEGER)` rồi chèn các tuple `(user, model, rating)`, còn `low_rated_users(conn, max_rating)` trả về danh sách các tên user không trùng, sắp xếp tăng dần, đã từng đánh giá `<= max_rating`. Hãy viết code trong từng hàm và `return` giá trị cần thiết.

**Ví dụ**

```python
conn = create_feedback_db([
    ("binh", "mini", 2),
    ("an", "gpt-4o", 5),
    ("an", "mini", 1),
    ("binh", "claude", 1),
])
low_rated_users(conn, 2)  # ["an", "binh"]
```

**Quy tắc**

- Luôn dùng placeholder `?` khi chèn dòng và truyền tham số truy vấn (tên có dấu nháy như `"O'Brien"` phải chạy đúng).
- Mỗi user thỏa điều kiện chỉ xuất hiện một lần, sắp xếp theo thứ tự bảng chữ cái tăng dần.
- Tính cả trường hợp biên `rating == max_rating` (`rating <= max_rating`).
- Trả về `[]` khi bảng rỗng hoặc không có đánh giá nào đạt ngưỡng.
