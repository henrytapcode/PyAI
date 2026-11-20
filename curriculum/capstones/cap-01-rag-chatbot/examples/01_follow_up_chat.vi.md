# Hội thoại FAQ 4 lượt có viết lại câu hỏi nối tiếp

**Những gì ví dụ minh họa:** Chạy một cuộc hội thoại FAQ 4 lượt trong đó câu hỏi nối tiếp ngắn được viết lại một cách tất định bằng cách ghép thêm câu hỏi người dùng gần nhất trước khi truy xuất, còn câu hỏi ngoài tài liệu sẽ từ chối gọn gàng.

**Từng bước một**
1. Dòng 6–24 đánh chỉ mục 8 trang FAQ cửa hàng thành 24 chunk theo câu bằng `FakeLLM(embed_dim=256)`.
2. Dòng 27–34 định nghĩa `rewrite_query(question, history)` để ghép câu hỏi người dùng gần nhất khi lượt mới dài tối đa 4 từ hoặc bắt đầu bằng `"what about"`, `"and"`, hoặc `"how about"`.
3. Dòng 37–60 định nghĩa `ask_turn(question, history)` để truy xuất top-2 chunk đạt `min_score=0.2`, kiểm tra trích dẫn `[n]` hợp lệ và thêm hai lượt vào `history`.
4. Dòng 63–76 chạy 4 lượt—một câu mở đầu về nhận hàng tại quầy, câu nối tiếp `"And photo ID?"`, một câu về giờ hỗ trợ, và một câu không có đáp án về crypto—rồi in thông tin từng lượt.

**Lưu ý:** Nếu không viết lại, `"And photo ID?"` sẽ thiếu từ khóa `"pickup"` trong prompt; ghép câu hỏi ở lượt 1 giúp lượt 2 truy xuất đúng `pickup.md` và trả lời `"Bring a photo ID at pickup. [1]"`, còn lượt 4 không có chunk vượt `min_score` nên trả `sources` rỗng.

**Tự thử:** Đổi lượt 1 thành `"How much does express delivery cost?"` và lượt 2 thành `"What about free shipping?"` để quan sát cả hai lượt đều truy xuất đúng `shipping.md`.
