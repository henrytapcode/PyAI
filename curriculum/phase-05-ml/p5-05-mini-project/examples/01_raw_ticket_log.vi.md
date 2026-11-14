# Kiểm tra log ticket thô

**Ví dụ này cho thấy:** Soi một DataFrame log ticket hỗ trợ thô gồm 240 dòng để kiểm tra kích thước, số ID trùng, ô thiếu theo cột, biến thể bẩn của `plan` và mức độ lệch lớp trước khi làm sạch.

**Từng bước**
1. Các dòng 7–24 định nghĩa `make_ticket_log(n=240, seed=21)` tạo dữ liệu thô có chuỗi chứa dấu phẩy ở `tokens`, vài ô thiếu, `ticket_id` lặp, nhãn `plan` lộn xộn và cột target leakage `escalated_to_oncall`.
2. Các dòng 27–34 in kích thước thô `(240, 7)`, `4` dòng trùng `ticket_id` và số ô thiếu (`tokens: 3`, `error_count: 2`).
3. Các dòng 36–41 in sáu biến thể bẩn của `plan` (`'free'`, `' Free'`, `'pro'`, `' PRO'`, `'enterprise'`, `'Enterprise '`) cùng tỉ lệ khẩn cấp `57/240 (0.237)`.

**Để ý:** `raw["plan"].value_counts()` tách 3 gói dịch vụ thật thành 6 nhóm riêng chỉ vì khoảng trắng thừa và viết hoa/thường không đồng nhất.

**Tự thử:** In thêm `raw["tokens"].head(8).tolist()` sau dòng 27 để thấy cả chuỗi có dấu phẩy như `'1,638'` lẫn giá trị `None` trong cột `tokens`.
