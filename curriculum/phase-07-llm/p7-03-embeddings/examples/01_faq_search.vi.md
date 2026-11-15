# Tìm kiếm ngữ nghĩa trên FAQ của cửa hàng

**Những gì ví dụ minh họa:** Embed danh sách FAQ một lần thành ma trận rồi trả lời câu hỏi của khách bằng xếp hạng top-1 qua tích vô hướng kết hợp ngưỡng điểm tối thiểu.

**Từng bước một**
1. Dòng 5–20 khai báo sáu câu `FAQS`, ba câu hỏi `QUERIES` (gồm một câu hỏi thời tiết không liên quan) và `MIN_SCORE = 0.3`.
2. Dòng 22–23 khởi tạo `FakeLLM(embed_dim=256)` và embed cả sáu FAQ trong một lần gọi thành `doc_matrix`.
3. Dòng 25–32 embed từng câu hỏi, chấm điểm toàn bộ FAQ một lượt bằng `doc_matrix @ q_vec`, rồi chọn hạng nhất qua `np.argsort(-scores, kind="stable")[0]`.
4. Dòng 30–32 in `"no good match"` khi `best_score < MIN_SCORE`, tránh trả về chính sách cửa hàng cho câu hỏi thời tiết lạc đề.

**Lưu ý:** `"Want full money back"` khớp ngay với `"Full refund available within 30 days."` (`0.471`) dù không trùng từ nào, vì `FakeLLM` ánh xạ `"money back"` về `"refund"`.

**Tự thử:** Hạ `MIN_SCORE` xuống `0.0` hoặc thêm câu hỏi thứ tư `"cheap vehicle insurance"` xem FAQ nào đứng đầu.
