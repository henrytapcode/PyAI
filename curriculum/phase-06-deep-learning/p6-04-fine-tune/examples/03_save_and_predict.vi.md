# Lưu, nạp lại và dự đoán ticket mới

**Bài này minh họa:** Fine-tune BERT-Tiny, lưu cả model lẫn tokenizer vào thư mục tạm bằng `save_pretrained()`, nạp lại ở chế độ offline và phân loại bốn ticket hoàn toàn mới.

**Từng bước**
1. Dòng 33–53 nạp model đã ghim (`id2label={0: "bug", 1: "billing"}`) và chạy 10 bước fine-tune bằng `AdamW(lr=5e-4)` trên 48 ticket tập train.
2. Dòng 62–66 mở một `tempfile.TemporaryDirectory()`, ghi trọng số, cấu hình và file tokenizer bằng `save_pretrained(tmp)` rồi nạp lại cả hai từ `tmp`.
3. Dòng 67–69 tạo `pipeline("text-classification", ...)` từ các object vừa nạp lại và in nhãn chữ cạnh từng ticket mới.

**Lưu ý:** Luôn lưu tokenizer cùng thư mục với model để lúc nạp lại, model nhận đúng bảng từ vựng ID và các token đặc biệt khớp nhau.

**Tự thử:** Thêm một câu pha trộn như `"App crashed while downloading my invoice"` vào `new_tickets` và xem model dự đoán nhãn nào.
