# So sánh keyword search và semantic search

**Những gì ví dụ minh họa:** So sánh số từ trùng chính xác (`kw`) với điểm cosine similarity (`cos`) cho ba truy vấn đồng nghĩa trên bốn tài liệu.

**Từng bước một**
1. Dòng 5–16 định nghĩa bốn tài liệu ngắn và ba truy vấn viết hoàn toàn bằng từ đồng nghĩa (`"affordable automobile"`, `"rapid computer"`, `"reimbursement bug"`).
2. Dòng 19–20 viết hàm `keyword_hits()` đếm số từ chữ thường xuất hiện ở cả truy vấn lẫn tài liệu.
3. Dòng 23–24 embed bốn tài liệu một lần thành `doc_matrix` bằng `FakeLLM(embed_dim=256)`.
4. Dòng 26–34 in bảng đối chiếu gọn gồm điểm `kw` và `cos` cho từng cặp `(query, doc)`.

**Lưu ý:** Toàn bộ cột `kw` đều bằng `0` vì truy vấn và tài liệu không chung từ chính xác nào, trong khi cosine similarity bắt đúng tài liệu đích (`0.866`, `0.707`, `0.707`).

**Tự thử:** Thêm từ `"car"` vào `QUERIES[0]` để thấy `kw` tăng từ `0` lên `1` ở `doc0`.
