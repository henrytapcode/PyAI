Cô Lan lưu mỗi học sinh dưới dạng một dict như `{"name": "An", "scores": [8, 7.5, 9]}`. Hãy hoàn thành các hàm dưới đây. Viết code bên trong hàm và `return` kết quả. Phần 3 của bài học chỉ hai mẹo bạn cần: `:.2f` và `sorted(..., key=...)`.

1. `average(scores)` trả về điểm trung bình của một list số. Với list rỗng thì trả về `0.0`.
2. `letter_grade(avg)` trả về xếp loại theo thang điểm 10:
   - `"A"` nếu `avg >= 8.5`, `"B"` nếu `avg >= 7`, `"C"` nếu `avg >= 5.5`, `"D"` nếu `avg >= 4`, còn lại là `"F"`.
3. `sort_key(row)` là hàm phụ để sắp xếp. `row` là một dict như `{"name": "An", "avg": 8.17}`. Trả về tuple `(-row["avg"], row["name"])`.
4. `build_report(students)` trả về một **list các chuỗi**, mỗi học sinh một chuỗi, như `"An: 8.17 (B)"`:
   - điểm trung bình hiển thị đúng 2 chữ số thập phân;
   - sắp xếp theo điểm trung bình giảm dần; nếu bằng điểm thì xếp theo tên (A đến Z);
   - lớp rỗng trả về list rỗng `[]`;
   - gợi ý: tạo list các dict có `"name"` và `"avg"`, rồi dùng `sorted(rows, key=sort_key)`.

Ví dụ:

```python
build_report([
    {"name": "An", "scores": [8, 7.5, 9]},
    {"name": "Binh", "scores": [9, 9.5, 8.5]},
])
# ["Binh: 9.00 (A)", "An: 8.17 (B)"]
```

Bấm **Kiểm tra** để chạy test.
