# Bộ nhớ đệm câu hỏi FAQ với key đã chuẩn hóa

**Ví dụ này cho thấy:** Dùng `FakeLLM` để cache 12 câu hỏi hỗ trợ khách hàng bằng key SHA-256 đã chuẩn hóa khoảng trắng, in từng dòng `HIT`/`MISS` và tổng `hit_rate`.

**Từng bước**
1. Dòng 9–21 định nghĩa `normalize_question` (cắt khoảng trắng hai đầu và gộp nhiều dấu cách liên tiếp) cùng `make_faq_key` (đóng gói `model`, `system` đã chuẩn hóa, `question` đã chuẩn hóa và `temperature=0.0` qua `json.dumps(..., sort_keys=True)` rồi băm SHA-256).
2. Dòng 24–45 khởi tạo `FakeLLM`, dictionary `cache` và danh sách 12 câu hỏi gồm các câu lặp lại lẫn biến thể thừa khoảng trắng như `'  What is   RAG? '`.
3. Dòng 47–68 tra cứu từng key, tăng `hits` hoặc gọi `client.chat(...)` khi `MISS`, in từng lượt và tóm tắt `hit_rate=0.50`.

**Để ý:** Câu `'  What is   RAG? '` trúng ngay entry đã lưu cho `'What is RAG?'` nhờ `normalize_question` gộp khoảng trắng trước khi băm, trong khi chữ hoa/thường và dấu câu vẫn được giữ nguyên.

**Tự thử:** Thêm một biến thể lặp của `"What is tool calling?"` (như `"  What is   tool calling?  "`) vào danh sách `questions` rồi chạy lại để xem `hit_rate` tăng từ `0.50` lên `0.54`.
