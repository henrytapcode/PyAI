# Class ChatSession giữ lịch sử hội thoại

**Điều cần thấy:** Bọc `FakeLLM` trong một dataclass `ChatSession` nhỏ để người dùng chỉ cần truyền câu hỏi mới, còn `history` và `total_tokens` được tự động cập nhật.

**Từng bước**
1. Dòng 7–16 định nghĩa `ChatSession` gồm `client`, `system`, `history` và `total_tokens`, dùng `__post_init__` để chèn `system` message ban đầu. Một `@dataclass` tự động gọi `__post_init__` ngay sau khi `__init__` được sinh tự động chạy xong—đây là chỗ đặt kiểm tra dữ liệu hoặc thiết lập trạng thái dẫn xuất.
2. Dòng 18–24 cài đặt phương thức `ask(text)`: thêm message `user`, gọi `self.client.chat(self.history)`, thêm câu trả lời `assistant`, cộng `resp.usage.total_tokens` rồi trả về chuỗi trả lời.
3. Dòng 27–32 chạy ba câu hỏi qua `session.ask(...)` và in câu trả lời cùng độ dài `history` tăng dần (`3`, `5`, `7`) sau mỗi lượt.
4. Dòng 34–35 in độ dài lịch sử cuối cùng (`7`) và tổng token (`208`).

**Lưu ý:** Mỗi lượt hội thoại thêm đúng hai phần tử vào `history` (một `user` và một `assistant`), nên ba lượt cộng thêm `system` ban đầu tạo thành `1 + 2 * 3 = 7` message.

**Thử tự sửa:** Truyền thêm `temperature=0.8` vào `self.client.chat(...)` cùng `FakeLLM(seed=3)` và kiểm tra độ dài `history` vẫn không đổi.
