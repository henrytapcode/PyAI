# Kiểm tra trích dẫn với danh sách chunk đã truy xuất

**Những gì ví dụ minh họa:** Dùng `FakeLLM(script=[...])` để giả lập ba tình huống: câu trả lời bám nguồn, câu trả lời bịa trích dẫn `[3]` khi chỉ có `2` chunk, và câu trả lời không có trích dẫn nào, rồi dùng Python gắn cờ cả hai lỗi.

**Từng bước một**
1. Dòng 7–15 định nghĩa `check_citations(answer, n_chunks)` tách các nhãn `[n]`, phân loại chỉ số hợp lệ `valid` (`1 <= n <= n_chunks`) với chỉ số ngoài phạm vi `invalid`, đồng thời bật cờ `missing: True` khi không có trích dẫn nào.
2. Dòng 18–28 chuẩn bị hai chunk đã truy xuất và cấu hình `FakeLLM` với ba câu trả lời tương phản.
3. Dòng 29–33 gọi `client.chat()` cho từng trường hợp và in ra từ điển kết quả kiểm tra.

**Lưu ý:** Chỉ kiểm tra có `[1]` hoặc truy cập thẳng `hits[n - 1]` đều dễ bỏ sót lỗi; `check_citations()` phát hiện cả trích dẫn không tồn tại `[3]` lẫn câu trả lời thiếu hoàn toàn nguồn trích dẫn.

**Tự thử:** Thêm câu trả lời kịch bản thứ tư `"Refunds take 30 days. [0] [2]"` để xem `[0]` bị đưa vào `invalid` còn `[2]` được nhận vào `valid`.
