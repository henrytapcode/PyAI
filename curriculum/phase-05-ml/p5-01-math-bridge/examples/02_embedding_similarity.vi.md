# Tìm tài liệu gần nhất bằng cosine similarity

**Nội dung minh họa:** So sánh vector câu hỏi với bốn embedding tài liệu 4 chiều nhỏ bằng cosine similarity để chọn tài liệu khớp nhất.

**Từng bước**
1. Dòng 4 định nghĩa vector `query` gồm 4 con số.
2. Dòng 6–11 lưu bốn vector tài liệu có gắn nhãn với cùng số chiều.
3. Dòng 15 tính độ dài câu hỏi `q_norm` một lần bằng `np.linalg.norm(query)` để không phải tính lại trong vòng lặp.
4. Dòng 17–24 chia tích vô hướng `query @ vec` cho `q_norm * np.linalg.norm(vec)`, in độ tương đồng đã làm tròn và cập nhật tài liệu khớp nhất.

**Lưu ý:** `refund_policy` đạt `0.99` vì các con số của nó hướng gần trùng với `query`, dù `shipping_faq` cũng có các giá trị dương tương đối gần.

**Tự thử:** Nhân `refund_policy` với `2.0` (kéo dài mũi tên gấp đôi) rồi chạy lại — để ý rằng cosine similarity vẫn giữ nguyên `0.99`.
