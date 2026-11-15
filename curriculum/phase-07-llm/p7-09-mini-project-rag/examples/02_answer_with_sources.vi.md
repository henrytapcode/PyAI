# Trả lời câu hỏi trực tiếp, diễn đạt khác và ngoài tài liệu

**Những gì ví dụ minh họa:** Chạy trọn luồng trả lời RAG trên ba kiểu câu hỏi thực tế—câu hỏi trực tiếp, câu paraphrase và câu ngoài kho kiến thức—kèm kiểm tra trích dẫn `[n]`.

**Từng bước một**
1. Dòng 18–25 dựng chỉ mục chunk theo câu một lần bằng `FakeLLM(embed_dim=256)`.
2. Dòng 28–50 cài đặt `answer_with_sources()` để lọc hit đạt `min_score=0.2`, gửi `Context:` cho `FakeLLM.chat()` và trích ra danh sách `source` hợp lệ từ `[n]`.
3. Dòng 56–65 chạy bot lần lượt trên ba câu `"direct"`, `"paraphrase"` và `"out_of_docs"`, rồi in câu trả lời và nguồn.

**Lưu ý:** Câu `"paraphrase"` (`"Can I get money back within a month?"`) vẫn kéo lên được `refunds.md`, nhưng `FakeLLM.chat()` chỉ đếm trùng từ thô (`>= 2` từ) không qua bảng từ đồng nghĩa nên trả về `"I don't know based on the provided context."` và `sources: []`.

**Tự thử:** Thay `"money back"` thành `"refunds"` ở câu hỏi thứ hai rồi chạy lại để thấy `sources` chuyển thành `['refunds.md']`.
