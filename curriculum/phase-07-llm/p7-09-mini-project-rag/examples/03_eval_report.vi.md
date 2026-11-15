# So sánh trên tập dev và báo cáo test một lần

**Những gì ví dụ minh họa:** So sánh ba cấu hình RAG trên `dev_set`, chọn cấu hình thắng cuộc (`sent k=2 m=0.2`) theo `facts`, chấm `test_set` đúng một lần và báo cáo trung thực mọi câu sai.

**Từng bước một**
1. Dòng 17–40 tách rạch ròi 12 câu eval thành `dev_set` (8 câu) và `test_set` (4 câu).
2. Dòng 56–92 chạy đánh giá một cấu hình `(mode, k, min_score)` và phân loại lỗi thành `"retrieval_miss"`, `"answer_miss"` hoặc `"no_refusal"`.
3. Dòng 99–113 so sánh cả ba ứng viên trên `dev_set` và chọn phương án thắng dựa hoàn toàn vào điểm dev.
4. Dòng 114–120 chấm `test_set` một lần với cấu hình đã chọn và in toàn bộ danh sách câu sai của cả dev lẫn test.

**Lưu ý:** Cấu hình thắng cuộc (`sent k=2 m=0.2`) đạt `5/6 (83%)` facts trên dev (`d6: answer_miss`, `d8: no_refusal`) và `2/3 (67%)` facts trên test (`t3: answer_miss`), cho thấy số đếm thô và lý do sai quan trọng hơn điểm 100%.

**Tự thử:** Thử đổi `min_score` thành `0.15` chỉ trên `dev_set` (tạm bỏ phần test)—kết quả dev có thay đổi gì không?
