# Lần theo lỗi biên khi debug

**Ví dụ này minh họa:** cách theo dõi bảng Watch (`idx`, `score` và `score > passing`) giúp phát hiện lỗi so sánh sai điều kiện biên.

**Từng bước**
1. `buggy_first_passing` kiểm tra `score > passing` thay vì `score >= passing`.
2. Khi `score` bằng `70` và `passing` bằng `70`, dòng watch in ra `check=False`, khiến vòng lặp bỏ qua chỉ số `1` và trả về `2` (`88`).
3. `fixed_first_passing` dùng `>=`, trả về đúng chỉ số `1`.

**Tự thử nghiệm:** đổi `passing` thành `90` rồi chạy lại để thấy cả hai hàm đều trả về `None`.
