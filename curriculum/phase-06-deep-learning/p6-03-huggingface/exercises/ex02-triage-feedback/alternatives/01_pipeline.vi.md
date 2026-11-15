# Đối chiếu với `pipeline()` (chỉ để tham khảo)

Lời giải này chỉ dùng để **đối chiếu**, **không** đạt Rule cấm gọi `transformers.pipeline` của đề bài — bài nộp của bạn vẫn phải tự viết từng bước như trong `solution.py`.

Cách này tạo `pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)` từ hai object `model` và `tokenizer` đã nạp sẵn thay vì tự gọi `tokenizer(...)`, `model(**batch)`, `torch.softmax` và `argmax`.

**Khi nào cách này đủ dùng:** Khi viết script thử nghiệm nhanh hoặc suy đoán thông thường mà chỉ cần nhãn và điểm số mặc định, `pipeline()` ngắn gọn hơn và tránh được lỗi quên `no_grad()` hay sai shape.

**Khi nào cần tự làm từng bước:** Khi bạn cần đọc logits thô (để chỉnh ngưỡng hay tính loss), kiểm soát padding/truncation theo ý mình, hoặc viết vòng lặp fine-tune trọng số model (`p6-04-fine-tune`), hãy viết rõ từng bước tokenizer + model như trong `solution.py`.
