Cô Lan lưu mỗi học sinh dưới dạng một dict như `{"name": "An", "scores": [8, 7.5, 9]}`. Nhiệm vụ của bạn là xây nửa đầu của công cụ bảng điểm: điểm trung bình, xếp loại và bảng điểm có xếp hạng. Trong editor đã có sẵn bốn khung hàm với các bước `# TODO`. Viết code bên trong hàm và `return` kết quả. Phần 4 và 5 của bài học chỉ hai mẹo bạn cần: `:.2f` và `sorted(..., key=...)`.

**Ví dụ**

```python
build_report([
    {"name": "An", "scores": [8, 7.5, 9]},
    {"name": "Binh", "scores": [9, 9.5, 8.5]},
])
# ["Binh: 9.00 (A)", "An: 8.17 (B)"]
```

| Hàm | Đầu vào | Đầu ra |
|---|---|---|
| `average([5, 6])` | list các số | `5.5` |
| `letter_grade(7.2)` | một số | `"B"` |
| `sort_key({"name": "An", "avg": 8.5})` | một dict row | `(-8.5, "An")` |
| `build_report(students)` | list các dict học sinh | list các dòng chữ |

**Quy tắc**

- `average(scores)` trả về điểm trung bình của một list số. Với list rỗng thì trả về `0.0`.
- `letter_grade(avg)` dùng thang điểm 10: `"A"` nếu `avg >= 8.5`, `"B"` nếu `avg >= 7`, `"C"` nếu `avg >= 5.5`, `"D"` nếu `avg >= 4`, còn lại là `"F"`.
- `sort_key(row)` là hàm phụ để sắp xếp. `row` là một dict như `{"name": "An", "avg": 8.17}`. Trả về tuple `(-row["avg"], row["name"])`.
- `build_report(students)` trả về một **list các chuỗi**, mỗi học sinh một chuỗi, như `"An: 8.17 (B)"`:
  - điểm trung bình hiển thị đúng 2 chữ số thập phân;
  - sắp xếp theo điểm trung bình giảm dần; nếu bằng điểm thì xếp theo tên (A đến Z);
  - lớp rỗng trả về list rỗng `[]`;
  - trả về các dòng, đừng in ra.

Bấm **Kiểm tra** để chạy test.
