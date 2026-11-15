# Dựng tập eval và chấm hit rate truy xuất

**Những gì ví dụ minh họa:** Chấm khả năng truy xuất top-2 trên tập eval 6 câu của cửa hàng, đồng thời bỏ qua câu không trả lời được khỏi mẫu số `hit_rate`.

**Từng bước một**
1. Dòng 5–13 khai báo kho kiến thức 7 chunk của cửa hàng (`refunds.md`, `shipping.md`, `warranty.md`, `hours.md`, `pickup.md`, `payment.md`, `loyalty.md`).
2. Dòng 15–22 định nghĩa `eval_set` gồm 6 câu hỏi, trong đó có câu diễn đạt khác từ (`q5`) và câu hỏi ngoài tài liệu về crypto (`q6` có `expected_source=None`).
3. Dòng 25–35 cài đặt `hit_rate(results, k)` để bỏ qua các dòng `None` trước khi đếm số câu trúng.
4. Dòng 38–54 embed toàn bộ tài liệu một lần bằng `FakeLLM(embed_dim=256)`, lấy top 2 nguồn cho từng câu, in bảng theo dõi và báo cáo `hit@2: 4/5 (0.8)`.

**Lưu ý:** `q5` bị trượt `refunds.md` ở `k=2` (`hours.md` và `payment.md` xếp trên), còn `q6` được ghi `skip` thay vì bị tính là truy xuất sai.

**Tự thử:** Đổi `[:2]` thành `[:3]` trong vòng lặp truy xuất và `hit_rate(results, 3)` ở dòng cuối để thấy `q5` chuyển thành trúng (`5/5 = 1.0`).
