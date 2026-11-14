# Tự tính softmax và nhãn rồi đối chiếu với `pipeline()`

**Điều cần thấy:** Tự chạy tokenizer và model với `model.eval()` và `torch.no_grad()`, tự tính `softmax` và `argmax`, rồi đối chiếu để thấy khớp hệt `pipeline()`.

**Từng bước**
1. Dòng 5–11 nạp `tokenizer` và `model` một lần từ cache và bật chế độ `model.eval()`.
2. Dòng 19–21 tokenize ba câu thành tensor PyTorch rồi chạy `model(**batch)` bên trong `with torch.no_grad():` để lấy `logits` thô.
3. Dòng 23–30 tính `torch.softmax(logits, dim=1)`, chọn chỉ số cao nhất từng hàng bằng `argmax(dim=1)` và đổi sang tên nhãn qua `model.config.id2label`.
4. Dòng 32–34 dựng `pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)` từ đúng hai object vừa nạp và kiểm tra `manual == from_pipe` in ra `match: True`.

**Lưu ý:** Bật `model.eval()` và `with torch.no_grad():` giúp bỏ qua việc theo dõi gradient khi suy đoán thủ công, và `torch.softmax(..., dim=1)` cho ra đúng điểm số giống hệt `pipeline()`.

**Thử tự sửa:** In thêm `logits.tolist()` trước bước `softmax` để thấy các điểm số thô đã tạo ra xác suất `0.991` hay `0.999`.
