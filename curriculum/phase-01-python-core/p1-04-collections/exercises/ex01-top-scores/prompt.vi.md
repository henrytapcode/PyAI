Công cụ tìm kiếm, hệ thống gợi ý hay bộ truy xuất đều làm cùng một việc: chấm điểm nhiều mục rồi giữ lại vài mục tốt nhất. Viết hàm `top_scores(scores, n)`. Hàm nhận một list số và một số nguyên `n`, rồi trả về một **list mới** gồm `n` số lớn nhất, **số lớn nhất đứng đầu**.

**Ví dụ**

| Lời gọi | Kết quả |
|---|---|
| `top_scores([0.5, 0.9, 0.7, 0.8], 2)` | `[0.9, 0.8]` |
| `top_scores([3, 1, 2], 5)` | `[3, 2, 1]` |
| `top_scores([], 3)` | `[]` |

**Quy tắc**

- Viết code bên trong hàm và dùng `return` để trả kết quả.
- Nếu `n` lớn hơn độ dài list, trả về tất cả các điểm (vẫn từ lớn đến nhỏ).
- Không được làm thay đổi list được truyền vào.

Bấm **Kiểm tra** để chạy test.
