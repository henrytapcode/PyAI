# Tạo và chia tập dữ liệu ticket

**Bài này minh họa:** Sinh 80 ticket hỗ trợ cân bằng hai lớp, chia tái lập thành train/val/test và đo độ dài token lớn nhất bằng tokenizer của BERT-Tiny.

**Từng bước**
1. Dòng 10–25 định nghĩa `make_tickets()`, trả về 40 ticket `bug` (nhãn `0`) và 40 ticket `billing` (nhãn `1`), gồm cả vài câu mơ hồ và câu dùng từ đồng nghĩa.
2. Dòng 28–36 xáo chỉ số bằng `torch.Generator` đặt seed `27` rồi tách 48 câu train, 16 câu validation và 16 câu test, in số lượng mỗi lớp ở từng tập.
3. Dòng 40–42 nạp `AutoTokenizer` đã ghim ở chế độ offline (`local_files_only=True`) và in độ dài token lớn nhất trên cả 80 ticket (`10`).

**Lưu ý:** Kiểm tra số lượng từng lớp ở mọi tập và độ dài token lớn nhất trước khi train giúp bạn phát hiện sớm tập bị lệch hoặc câu bị cắt cụt trước khi đưa vào model.

**Tự thử:** Đổi `manual_seed(27)` thành `manual_seed(0)` và xem tỉ lệ hai lớp trong `val` và `test` thay đổi thế nào.
