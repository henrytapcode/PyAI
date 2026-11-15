# Bot hỏi đáp chính sách cửa hàng

**Những gì ví dụ minh họa:** Trả lời các câu hỏi chính sách từ bốn tài liệu nhỏ kèm `sources` đã kiểm chứng, đồng thời bỏ qua hẳn lời gọi LLM khi câu hỏi nằm ngoài phạm vi.

**Từng bước một**
1. Dòng 7–12 lưu bốn đoạn chính sách ngắn của cửa hàng, mỗi đoạn gắn metadata `source` là tên file nguồn.
2. Dòng 15–22 kế thừa `FakeLLM` thành `CountingLLM` để đếm xem `chat()` thực sự được gọi bao nhiêu lần.
3. Dòng 25–47 định nghĩa `ask_bot()`, thực hiện truy xuất top-`k`, trả về sớm `"I don't know."` nếu điểm cao nhất dưới `min_score=0.2`, còn không thì dựng prompt `Context:` và ánh xạ trích dẫn `[n]` về `sources`.
4. Dòng 50–62 embed tất cả tài liệu một lần rồi thử hai câu hỏi chính sách cùng một câu hỏi giảm giá ngoài phạm vi.

**Lưu ý:** Với `"Do you offer student discounts?"`, điểm truy xuất cao nhất không đạt `min_score` nên `ask_bot()` trả `"I don't know."` và `Total chat calls` giữ ở mức `2` thay vì `3`.

**Tự thử:** Hạ `min_score` xuống `0.0` trong `ask_bot()` để thấy `Total chat calls` tăng lên `3` trong khi model vẫn từ chối trả lời dựa trên ngữ cảnh.
