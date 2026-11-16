# Lớp RagService kết hợp tính điểm bằng ma trận NumPy

**Cách hoạt động:** Thay vì giữ `doc_vecs` trong closure và lặp bằng hàm `cosine` thuần Python, cách này gói phần lập chỉ mục và truy xuất vào lớp `RagService` dùng mảng NumPy 2 chiều và `np.argsort(-scores, kind="stable")`.

**Khi nào nên chọn:** Cấu trúc này mở rộng tốt khi số tài liệu tăng lên (nhân ma trận với vector nhanh hơn nhiều so với vòng lặp Python qua hàng nghìn tài liệu) và giữ route FastAPI gọn nhẹ, đổi lại phải phụ thuộc NumPy và viết thêm lớp trung gian với tập tài liệu nhỏ.
