Bây giờ là thống kê cho cả lớp. `average` và `letter_grade` đã được viết sẵn trong starter. Hãy hoàn thành `class_stats(students)`. Viết code bên trong hàm và `return` kết quả.

Hàm trả về một dict với các khóa sau:

| Khóa | Giá trị |
|---|---|
| `"count"` | số học sinh |
| `"mean"` | trung bình của các điểm trung bình của mọi học sinh |
| `"best"` | **tên** học sinh có điểm trung bình cao nhất |
| `"worst"` | **tên** học sinh có điểm trung bình thấp nhất |
| `"grade_counts"` | dict có **đủ năm** loại `"A"` đến `"F"` và số học sinh mỗi loại (0 nếu không có) |

Các trường hợp biên:

- Nếu nhiều học sinh cùng đứng đầu (hoặc cùng cuối), chọn người có tên đứng trước theo bảng chữ cái.
- Học sinh có `scores` rỗng có điểm trung bình `0.0` (loại `"F"`).
- Lớp rỗng: `{"count": 0, "mean": 0.0, "best": None, "worst": None, "grade_counts": {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}}`.

Ví dụ:

```python
class_stats([
    {"name": "An", "scores": [8, 7.5, 9]},
    {"name": "Binh", "scores": [9, 9.5, 8.5]},
])
# {"count": 2, "mean": 8.583..., "best": "Binh", "worst": "An",
#  "grade_counts": {"A": 1, "B": 1, "C": 0, "D": 0, "F": 0}}
```

Bấm **Check** để chạy test.
