# Prompt template

**Ví dụ này cho thấy:** một object nhớ các thiết lập (đoạn template của nó) và còn đếm xem nó đã được dùng bao nhiêu lần.

**Từng bước**
1. Dòng 3–6 lưu ba attribute. `template` là đoạn text có placeholder (chỗ trống để điền) `{topic}` và `{audience}`; `uses` bắt đầu từ 0.
2. Dòng 9 cộng 1 vào `self.uses` mỗi lần `fill` chạy, nên object tự đếm số lần gọi của chính nó.
3. Dòng 10–11 thay lần lượt hai placeholder rồi trả về prompt hoàn chỉnh.
4. Dòng 17–18 tạo hai template khác nhau từ một class.
5. Dòng 20–22 điền nội dung vào. `explain` được dùng hai lần còn `quiz` một lần.
6. Dòng 23–24 in các object ra. `__repr__` hiện `uses`, nên bạn thấy được số lần dùng.

**Để ý:** đoạn placeholder như `"{topic}"` nằm trong một chuỗi thường, không phải f-string, nên Python để yên dấu ngoặc nhọn và `replace` tìm thấy được chúng.

**Tự thử:** tạo `summary = PromptTemplate("summary", "Summarise {topic} for {audience}.")`, điền một lần rồi in ra. Bạn sẽ thấy `uses=1`.
