# Làm sạch prompt

**Ví dụ này cho thấy:** chuẩn hóa text bằng `lower()`, `split()` và `join()`, rồi dùng `in` để phát hiện prompt trùng.

**Từng bước**
1. Dòng 2–4 định nghĩa `normalize(text)`. `text.lower()` đổi mọi thứ thành chữ thường, `.split()` cắt thành các từ và bỏ hết dấu cách thừa, còn `" ".join(words)` ghép các từ lại với đúng một dấu cách.
2. Dòng 7–11 chứa ba prompt thô. Hai prompt đầu chỉ khác nhau ở chữ hoa và dấu cách. Prompt thứ ba là một yêu cầu khác.
3. Dòng 13–20 lặp qua các prompt. Mỗi prompt được làm sạch trước (dòng 15), rồi `clean in seen` hỏi xem ta đã có đúng đoạn text đó chưa.
4. Dòng 19 thêm prompt mới vào `seen`; dòng 22 in ra còn lại bao nhiêu prompt khác nhau.

**Để ý:** phép so sánh chỉ đúng *sau khi* làm sạch. `"SUMMARIZE this text"` và `"   Summarize THIS   text  "` là hai chuỗi khác nhau, nhưng bản đã chuẩn hóa của chúng bằng nhau. Cùng mẹo này giúp một ứng dụng AI cache câu trả lời cho các câu hỏi lặp lại.

**Tự thử:** thêm `"summarize   this TEXT"` vào `raw_prompts`. Hãy đoán kết quả rồi chạy.
