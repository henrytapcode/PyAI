Viết hàm `grade(score)` đổi điểm (từ 0 đến 100) thành chữ cái xếp loại:

| Điểm | Xếp loại |
|---|---|
| từ 90 trở lên | `"A"` |
| 80 đến 89 | `"B"` |
| 70 đến 79 | `"C"` |
| 60 đến 69 | `"D"` |
| dưới 60 | `"F"` |

Hãy viết code **bên trong hàm** và dùng `return` để trả về kết quả. Bạn sẽ học hàm bài bản ở bài 5; bây giờ chỉ cần giữ nguyên dòng `def` và viết phần thân.

Chú ý các mốc: `90` là `"A"`, còn `89` là `"B"`.

**Ví dụ**

| Gọi hàm | Trả về |
|---|---|
| `grade(95)` | `"A"` |
| `grade(80)` | `"B"` |
| `grade(42)` | `"F"` |

**Quy tắc**
- Trả về một trong các chuỗi `"A"`, `"B"`, `"C"`, `"D"`, `"F"`.
- Điểm luôn là số nguyên từ 0 đến 100.
