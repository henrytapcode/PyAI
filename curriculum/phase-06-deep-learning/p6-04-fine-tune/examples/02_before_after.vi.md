# Đo tỉ lệ đoán đúng (accuracy) trước và sau khi fine-tune

**Bài này minh họa:** Chấm điểm bộ đầu phân loại (classification head) khởi tạo ngẫu nhiên của BERT-Tiny trên tập test (`0.562`), fine-tune 10 epoch full-batch bằng `AdamW` rồi đo mức tăng (`0.938`).

**Từng bước**
1. Dòng 28–34 định nghĩa `accuracy()`, bật `model.eval()` và `torch.no_grad()` để tắt dropout và không ghi đồ thị gradient.
2. Dòng 43–51 nạp tokenizer và model nền đã ghim (`torch.manual_seed(0)` ngay trước khi nạp) với `num_labels=2` cùng `id2label`/`label2id`.
3. Dòng 53 đo `before` (`0.562`), dòng 58–63 chạy 10 bước full-batch dùng `out = model(**train_batch, labels=train_y_t)` và `AdamW(lr=5e-4)`, rồi dòng 65–68 in `before`, `after` và `gain`.

**Lưu ý:** Đặt `torch.manual_seed(0)` ngay trước `from_pretrained()` giúp cả trọng số ngẫu nhiên của classification head lẫn dropout lúc train đều lặp lại được y hệt.

**Tự thử:** Đổi `lr=5e-4` thành `lr=1e-1` rồi xem tỉ lệ đoán đúng sau khi train không thể tăng ổn định như thế nào.
