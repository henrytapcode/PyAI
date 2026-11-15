# Bộ parse JSON chống nhiễu

**Ví dụ này minh họa:** Cắt lấy object JSON từ phản hồi lẫn tạp chất của LLM (fence markdown và câu dẫn) và ném `ValueError` rõ ràng khi phản hồi hỏng hoặc không có JSON.

**Từng bước**
1. Dòng 7–19 định nghĩa `extract_json()` tìm dấu `{` đầu tiên và `}` cuối cùng, parse đoạn cắt bằng `json.loads()`, rồi kiểm tra kết quả phải là `dict`.
2. Dòng 22–28 chuẩn bị năm câu trả lời mẫu gồm JSON trần, JSON trong fence, có câu dẫn, JSON lỗi cú pháp và văn xuôi thuần.
3. Dòng 30–37 đọc lần lượt năm phản hồi từ `FakeLLM(script=...)` rồi in dict đã parse hoặc thông báo `ValueError`.

**Điểm cần chú ý:** Vì `extract_json()` quy cả `json.JSONDecodeError` lẫn trường hợp thiếu ngoặc về `ValueError`, nơi gọi chỉ cần một khối `except ValueError` duy nhất.

**Tự thử:** Thêm phần tử thứ sáu `'["not", "an", "object"]'` vào `scripted_replies` để xem thông báo lỗi tương ứng.
