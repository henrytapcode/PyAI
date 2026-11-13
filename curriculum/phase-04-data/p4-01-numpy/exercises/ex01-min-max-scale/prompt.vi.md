Chuẩn hóa (feature scaling) đưa các con số về cùng thang `[0, 1]` trước khi đưa vào mô hình. Hãy hoàn thành `min_max_scale(values)` bằng cách thay mọi ô trống `___` để dịch chuyển và co giãn `values` theo công thức `(values - min) / (max - min)`. Đặt code bên trong hàm và `return` kết quả.

**Ví dụ**

| đầu vào | đầu ra |
|---|---|
| `np.array([10, 20, 30])` | `array([0.0, 0.5, 1.0])` |

**Quy tắc**
- Giữ nguyên `shape` của `values` (chạy đúng cho cả mảng 1D và 2D).
- Không sửa trực tiếp mảng đầu vào.
- Giả sử `values.max() > values.min()`.
