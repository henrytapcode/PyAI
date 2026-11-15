# Chấm fact và độ trung thực câu trả lời

**Những gì ví dụ minh họa:** Chạy trọn pipeline RAG với `FakeLLM` trên tập eval để đo `facts`, `faithful` và khả năng từ chối `"I don't know"`, sau đó bắt một câu trả lời bịa mô phỏng bằng `script`.

**Từng bước một**
1. Dòng 25–45 định nghĩa `content_words()` và `score_answer()`, kiểm tra chuỗi con `expected_facts` ở dạng chữ thường và đối chiếu mọi từ nội dung (`len >= 4`, bỏ trích dẫn `[n]`) với `context`.
2. Dòng 48–66 truy xuất top 2 chunk cho mỗi câu, gọi `client.chat(...)` rồi in `facts`, `faithful` và `idk` cho `q1`–`q6`.
3. Dòng 69–76 tạo một `FakeLLM(script=[...])` riêng trả về `"Refunds are issued within 30 days with free courier pickup. [1]"` rồi chấm với `q1_context`.

**Lưu ý:** Câu trả lời từ `script` vẫn chứa `"30 days"` nên đạt `facts=1.0`, nhưng `faithful` đã bắt lỗi `False` và liệt kê `['with', 'free', 'courier', 'pickup']` là các từ không có trong ngữ cảnh.

**Tự thử:** Đổi câu trong `script` thành `"Refunds are issued within 30 days of purchase. [1]"` để thấy `faithful` chuyển lại thành `True` với `unsupported: []`.
