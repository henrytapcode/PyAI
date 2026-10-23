# Xếp hạng học sinh

**Ví dụ này cho thấy:** cách xếp hạng một list các dict bằng `sorted(..., key=...)` với key dạng tuple, và chuyện gì xảy ra khi hai học sinh bằng điểm.

**Từng bước**
1. Dòng 2–5 là hàm `average` bạn đã biết.
2. Dòng 8–9 định nghĩa `sort_key`. Hàm nhận một dòng (row) và trả về tuple `(-avg, name)`. Dấu trừ đảo thứ tự, nên điểm trung bình cao nhất đứng đầu.
3. Dòng 12–17 chứa dữ liệu thô. Mai và Zoe đều có điểm trung bình `7.0`.
4. Dòng 19–21 biến mỗi học sinh thành một row nhỏ `{"name": ..., "avg": ...}`. Sắp xếp dễ hơn trên các row đã có sẵn điểm trung bình, vì ta chỉ tính nó một lần.
5. Dòng 24 sắp xếp các row. `key=sort_key` **không có dấu ngoặc**: ta truyền chính hàm đó, và Python tự gọi nó trên từng row.
6. Dòng 23–26 in danh sách có đánh số. `rank` bắt đầu từ 1 và tăng thêm 1 sau mỗi dòng.

**Để ý:** Mai và Zoe cùng điểm trung bình, nên Python so sánh giá trị thứ hai của tuple, tức là tên. `"Mai"` đứng trước `"Zoe"` theo bảng chữ cái, nên Mai được liệt kê trước.

**Tự thử:** đổi điểm của Zoe thành `[10, 10]`. Hãy đoán ai đứng hạng 1 bây giờ (Zoe, với `10.00`).
