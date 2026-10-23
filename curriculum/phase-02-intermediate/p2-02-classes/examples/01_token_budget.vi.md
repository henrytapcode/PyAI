# Ngân sách token

**Ví dụ này cho thấy:** một class, hai object. Mỗi tính năng (`chat`, `search`) có một `TokenCounter` riêng với giới hạn riêng và tổng đang chạy riêng.

**Từng bước**
1. Dòng 3–6 là `__init__`. Chúng lưu ba attribute `name`, `limit` và `total` (bắt đầu từ 0).
2. Dòng 8–9 là `add`. Nó thay đổi object: `self.total += n`.
3. Dòng 11–12 là `remaining`. Nó chỉ đặt câu hỏi và **trả về** câu trả lời.
4. Dòng 14–15 là `__repr__`, nên `print(chat)` hiện một dòng dễ đọc thay vì địa chỉ bộ nhớ.
5. Dòng 18–19 tạo hai object từ cùng một class. Dòng 21–24 cộng số token vào từng object trong vòng lặp.
6. Dòng 28–32 duyệt qua một list các object. Cùng một đoạn code chạy cho cả hai vì cả hai có cùng các method.

**Để ý:** `chat` kết thúc ở 870 còn `search` ở 220. Cộng vào object này không làm đổi object kia, vì mỗi object có `total` riêng.

**Tự thử:** thêm bộ đếm thứ ba, `summary = TokenCounter("summary", 50)`, gọi `summary.add(60)`, rồi thêm nó vào list ở vòng lặp cuối. Nó phải báo vượt ngân sách 10.
