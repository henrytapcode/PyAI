# Một bảng các trường hợp

**Ví dụ này cho thấy:** ý tưởng đằng sau `parametrize`. Thay vì một test cho mỗi input, bạn viết một bảng các cặp `(input, expected)` và chạy cùng một phép kiểm tra trên mọi dòng, rồi báo cáo dòng nào thất bại.

**Từng bước**
1. Dòng 2–3 là hàm được kiểm tra, `normalize_spaces`.
2. Dòng 6–12 là bảng. Mỗi dòng là một trường hợp: một văn bản bình thường, tab và xuống dòng, một văn bản rỗng, chỉ có khoảng trắng, và một từ đơn.
3. Dòng 14–21 chạy từng dòng. Dòng khớp thì cộng một vào `passed`; dòng không khớp được lưu lại cùng văn bản, kỳ vọng và kết quả.
4. Dòng 23–25 in các thất bại trước rồi in tổng số.

**Lưu ý:** dòng cuối thất bại, nhưng hàm lại đúng. Kỳ vọng `"one "` có một khoảng trắng mà hàm đã bỏ đi một cách chính xác. Một test đỏ nghĩa là "hãy nhìn ở đây", và bug có thể nằm ở chính test. Hãy đọc cả hai vế trước khi sửa bất kỳ thứ gì.

**Thử tự làm:** sửa dòng cuối thành `("one", "one")`. Báo cáo sẽ ghi `5 passed, 0 failed`.
