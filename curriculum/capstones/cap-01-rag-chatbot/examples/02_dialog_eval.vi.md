# Đánh giá golden dialog và so sánh với baseline

**Những gì ví dụ minh họa:** Chấm hai golden dialog gồm 2 lượt mỗi hội thoại theo từng lượt và đối chiếu với bản baseline để chỉ rõ cả các ca mới sửa (`fixed`) lẫn ca mới hỏng (`broken`).

**Từng bước một**
1. Dòng 17–32 khai báo hai golden dialog (`d1` có câu hỏi nối tiếp, `d2` có một câu trả lời được và một câu cần từ chối).
2. Dòng 44–77 định nghĩa `eval_dialogs(rewrite, min_score)` để chấm từng lượt theo `expected_source`, `expected_facts`, hoặc kỳ vọng từ chối.
3. Dòng 80–81 chạy bản baseline (`rewrite=False, min_score=0.2`) và bản mới (`rewrite=True, min_score=0.35`).
4. Dòng 83–92 tính danh sách `fixed` và `broken` rồi in bảng so sánh ngắn.

**Lưu ý:** Cả hai lần chạy đều đạt tổng `3/4 (75%)`, nhưng bảng đối chiếu từng lượt vạch ra đánh đổi ẩn: viết lại câu hỏi sửa được `d1#t2`, trong khi nâng `min_score` lên `0.35` lại làm hỏng `d2#t1`.

**Tự thử:** Đổi `min_score=0.35` ở dòng 81 thành `min_score=0.25` để thấy `d1#t2` vẫn đạt còn `broken` trở về `[]`.
