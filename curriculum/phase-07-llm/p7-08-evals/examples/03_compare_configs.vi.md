# So sánh hai cấu hình RAG trên cùng tập eval

**Những gì ví dụ minh họa:** Chạy đối chiếu `k=1` và `k=3` trên cùng tập eval 6 câu, in bảng tổng bằng số đếm kèm phần trăm, và liệt kê từng câu hỏi đã đổi kết quả.

**Từng bước một**
1. Dòng 48–75 định nghĩa `run_config(k)` để truy xuất top-`k` chunk từ `doc_matrix` đã embed sẵn, sinh câu trả lời và tổng hợp số đếm.
2. Dòng 78–86 chạy `k=1` và `k=3` rồi in bảng tóm tắt gọn với số đếm `hit@k`, `facts`, `faithful` và `idk`.
3. Dòng 88–91 đối chiếu cặp `(hit, facts)` của từng câu giữa `k=1` và `k=3` để in ra các câu bị thay đổi.

**Lưu ý:** Tăng `k` từ `1` lên `3` giúp `hit@k` (`3/5` lên `5/5`) và `facts` (`3/5` lên `4/5`) tăng nhờ sửa được `q2`, nhưng lại làm `idk` tụt từ `1/1` xuống `0/1` vì `payment.md` lọt vào top 3 của `q6` và làm model trả lời sai.

**Tự thử:** Thêm `k=2` vào vòng lặp `for k in (1, 3):` để so dòng tổng kết của `k=2` với `k=1` và `k=3`.
