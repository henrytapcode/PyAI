# Ghi log một lần gọi LLM

**Ví dụ này cho thấy:** một hàm gọi model (giả), thử lại khi bị timeout, và ghi log mỗi lần thử dưới dạng các trường `key=value`: model, lần thử, độ trễ và kích thước câu trả lời.

**Từng bước**
1. Dòng 5–11 thiết lập logging một lần và tạo logger `app.llm`. Format hiển thị mức log, tên logger và nội dung.
2. Dòng 13–14 tạo dữ liệu giả: câu trả lời đầu tiên là timeout, và một đồng hồ giả cho cùng các mốc thời gian ở mỗi lần chạy.
3. Dòng 17–21 là model giả. Nó raise `TimeoutError` khi câu trả lời là `"TIMEOUT"`.
4. Dòng 25–31 lặp qua các lần thử. Timeout được ghi ở mức `WARNING` (`llm_retry`) và vòng lặp thử lại bằng `continue`.
5. Dòng 32–37 tính độ trễ từ đồng hồ giả, ghi một dòng `INFO` (`llm_call`) và trả về câu trả lời.
6. Dòng 38 chỉ chạy nếu mọi lần thử đều thất bại: đó là `ERROR`, vì thao tác đã thất bại.

**Để ý:** mỗi loại sự kiện có một mức log khác nhau, và mỗi thông điệp bắt đầu bằng một từ cố định (`llm_retry`, `llm_call`, `llm_failed`). Nhờ vậy sau này dễ tìm và đếm các dòng.

**Tự thử:** đổi câu trả lời đầu tiên ở dòng 13 thành một đoạn văn bình thường. Dòng `WARNING` phải biến mất và dòng `INFO` phải ghi `attempt=1`.
