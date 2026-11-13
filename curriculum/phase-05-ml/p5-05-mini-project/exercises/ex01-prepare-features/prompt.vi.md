Viết hàm `prepare_features(raw)` để làm sạch `DataFrame` log ticket hỗ trợ thô thành cặp mảng NumPy `(X, y)` đồng thời loại bỏ cột target leakage. Viết code bên trong hàm và `return` `(X, y)`.

**Ví dụ**

Đầu vào `raw`:

```text
  ticket_id  plan tokens  error_count  hours_since_deploy  escalated_to_oncall  urgent
0       t01   PRO  1,200          2.0                 4.5                    1       1
1       t01  free    500          0.0                10.0                    0       0
```

Giá trị trả về `(X, y)`:
- `X`: `array([[1200., 2., 4.5, 1.]])` (`float64`, shape `(1, 4)`)
- `y`: `array([1])` (`"int64"`, shape `(1,)`)

**Quy tắc**

- Không sửa đổi trực tiếp `raw`.
- Chuẩn hóa `plan` bằng `.astype(str).str.strip().str.lower()` rồi ánh xạ `"free" -> 0.0`, `"pro" -> 1.0`, `"enterprise" -> 2.0` (`plan_code`). Tên gói lạ thành thiếu (`NaN`) và bị loại bỏ.
- Xóa dấu phẩy `","` ở `tokens` (bằng `.astype(str).str.replace(",", "", regex=False)`) rồi ép kiểu `tokens`, `error_count` và `hours_since_deploy` sang số bằng `pd.to_numeric(..., errors="coerce")`.
- Bỏ các dòng trùng `ticket_id` và giữ lại dòng đầu tiên (`keep="first"`).
- Bỏ các dòng bị thiếu ở `tokens`, `error_count`, `hours_since_deploy`, `plan_code` hoặc `urgent`.
- Loại bỏ `escalated_to_oncall` (target leakage) khỏi `X`.
- Trả về `(X, y)` trong đó `X` là mảng NumPy 2D kiểu `"float64"` với các cột theo đúng thứ tự `["tokens", "error_count", "hours_since_deploy", "plan_code"]` và `y` là mảng NumPy 1D kiểu `"int64"` của nhãn `urgent` (`0` hoặc `1`). Nếu toàn bộ dòng bị loại, trả về shape `(0, 4)` cho `X` và `(0,)` cho `y`.
