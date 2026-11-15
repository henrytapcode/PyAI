# Vòng lặp với cosine() và sorted()

**Cách hoạt động:** Thay vì chuyển embedding thành ma trận NumPy để tính `D @ q` và `np.argsort`, cách này duyệt qua từng vector trong `doc_vecs`, chấm điểm bằng `pyai_llm.cosine()`, lọc theo `min_score`, rồi sắp xếp bằng `key=lambda pair: (-pair[1], pair[0])`.

**Khi nào nên chọn:** Phù hợp khi bạn đang làm việc với list Python thuần, không muốn phụ thuộc NumPy hoặc cần hỗ trợ cả vector chưa chuẩn hóa (vì `cosine()` tự chia cho độ dài vector). Với hàng nghìn tài liệu, lời giải ma trận `D @ q` sẽ nhanh hơn nhiều.
