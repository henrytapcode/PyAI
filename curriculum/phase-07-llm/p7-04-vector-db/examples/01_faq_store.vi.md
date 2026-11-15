# Kho vector FAQ song ngữ

**Những gì ví dụ minh họa:** Lưu tám chunk FAQ song ngữ kèm metadata `topic` và `lang` vào `VectorStore`, rồi trả lời các câu hỏi không lọc và có lọc metadata.

**Từng bước một**
1. Dòng 7–54 định nghĩa `Hit` và `VectorStore`, kiểm tra trùng ID, embed cả lô một lần trong `add()` và lọc trước metadata trong `search()`.
2. Dòng 57–69 khai báo tám `CHUNKS` song ngữ kèm metadata `topic` và `lang` rồi nạp tất cả bằng một lần gọi `store.add(...)`.
3. Dòng 71–79 chạy ba truy vấn: hai câu hỏi đồng nghĩa không lọc (`"money back"` và `"affordable vehicle"`) và một câu hỏi lọc `lang == "vi"` cùng `topic == "support"`.

**Lưu ý:** Ở câu hỏi thứ ba, `faq2` (`"Fast laptop repair in two days."`) bị loại trước khi xếp hạng vì `lang` là `"en"`, nhờ vậy `faq6` đứng hạng nhất gọn gàng.

**Tự thử:** Đổi bộ lọc ở câu hỏi thứ ba thành `{"lang": "en", "topic": "support"}` và kiểm tra rằng `faq2` và `faq4` được trả về.
