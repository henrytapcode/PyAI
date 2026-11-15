# Xếp hạng thuần Python bằng `cosine()` và `sorted()`

Cách tiếp cận này không dùng NumPy mà lưu các vector embedding dưới dạng list Python thuần, chấm điểm từng chunk bằng `pyai_llm.cosine(vec, q_vec)` rồi sắp xếp cặp `(score, idx)` theo khóa `(-score, idx)` để giữ nguyên thứ tự ổn định khi bằng điểm. Cách này dễ đọc và chạy được ngay cả trong môi trường tối giản không cài NumPy, còn phép nhân ma trận NumPy trong `solution.py` sẽ nhanh hơn nhiều khi chỉ mục vượt quá vài nghìn chunk.
