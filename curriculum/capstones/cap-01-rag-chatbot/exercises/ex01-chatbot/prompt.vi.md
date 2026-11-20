Hãy cài đặt class `ChatBot` có trạng thái (`__init__` và `ask`) bằng hai hàm `build_index` và `retrieve` đã cho sẵn trong `starter.py`. Khác với các đoạn code rời trong bài học, class của bạn phải gom toàn bộ luồng vào trạng thái riêng của từng bot, ghim `system` prompt bên ngoài `history` khi cắt bớt, từ chối câu ngoài phạm vi mà không gọi `client.chat`, lọc các citation `[n]` hợp lệ, và viết lại câu nối tiếp từ câu gốc người dùng gõ thay vì câu đã viết lại. Hãy viết code bên trong `ChatBot` và `return` dict kết quả từ `ask`.

**Ví dụ**

```python
bot = ChatBot(docs, client)

bot.ask("How long are store pickup orders held?")
# -> {
#     "answer": "Unclaimed orders are held at the counter for 7 days. [2]",
#     "sources": ["pickup.md"],
#     "rewritten": "How long are store pickup orders held?",
# }

bot.ask("And photo ID?")
# -> {
#     "answer": "Bring a photo ID at pickup. [1]",
#     "sources": ["pickup.md"],
#     "rewritten": "How long are store pickup orders held? And photo ID?",
# }

bot.ask("Do you offer cryptocurrency billing?")
# -> {
#     "answer": "I don't know based on the provided context.",
#     "sources": [],
#     "rewritten": "Do you offer cryptocurrency billing?",
# }
```

**Quy tắc**

- Giữ nguyên hai hằng `REFUSAL = "I don't know based on the provided context."` và `DEFAULT_SYSTEM = "Answer only from the shop FAQ context and cite sources as [n]."`, và đúng chữ ký `ChatBot(docs, client, system_prompt=DEFAULT_SYSTEM, k=2, min_score=0.2, max_history_tokens=60)`.
- Trong `__init__`, gọi `build_index(docs, client)` **một lần** để chỉ embed các chunk đúng một lần trong suốt vòng đời bot, và cấp cho mỗi bot một `self.history: list[dict]` riêng (chỉ chứa các lượt `{"role": "user"|"assistant", "content": ...}`, không chứa `system`).
- Trong `ask(question)`: `.strip()` chuỗi `question` và raise `ValueError` nếu rỗng hoặc chỉ toàn khoảng trắng.
- **Viết lại câu nối tiếp:** lấy nội dung `"user"` gần nhất trong `self.history` (câu gốc người dùng gõ, không phải câu đã viết lại). Nếu có và câu mới có `<= 4` từ, từ đầu tiên (viết thường) là `"and"`, hoặc bắt đầu bằng `"what about "` / `"how about "` (không phân biệt hoa thường) thì đặt `rewritten = f"{prev_user} {question}"`; ngược lại `rewritten = question`.
- Truy xuất bằng `retrieve(self.index, rewritten, self.client, self.k, self.min_score)`. Nếu không có hit nào, đặt `answer = REFUSAL` và `sources = []` và **không gọi `client.chat`**.
- Nếu có hit, gọi `client.chat` **một lần** với `temperature=0.0` và `messages = [{"role": "system", "content": system_prompt + "\n\nContext:\n[1] <text>\n[2] <text>..."}, *self.history, {"role": "user", "content": rewritten}]`.
- **Citation:** tìm mọi `[n]` trong `answer`, chỉ giữ các chỉ số thỏa `1 <= n <= len(hits)`, và gom `hit["source"]` tương ứng (không trùng, theo thứ tự xuất hiện) vào `sources`. Trả về `answer` nguyên văn.
- **Lịch sử & cắt bớt:** sau mỗi lần gọi `ask` (kể cả khi từ chối), thêm `{"role": "user", "content": question}` rồi `{"role": "assistant", "content": answer}` vào `self.history`. Khi `count_tokens(system_prompt) + sum(count_tokens(m["content"]) for m in self.history) > max_history_tokens` và `len(self.history) > 2`, bỏ lượt cũ nhất (`self.history.pop(0)`). `system` prompt không bao giờ bị bỏ, và cặp lượt mới nhất luôn được giữ.
