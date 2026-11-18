# Train theo mini-batch với DataLoader và chia train/val/test

**Điều cần thấy:** Chia dữ liệu tổng hợp thành ba tập train/validation/test, duyệt từng mini-batch đã xáo trộn bằng `DataLoader`, theo dõi tỉ lệ đoán đúng (accuracy) trên validation mỗi 5 epoch và chỉ đánh giá test set một lần ở cuối.

**Từng bước**
1. Dòng 5–16 tạo 200 điểm 2D đã xáo trộn ngẫu nhiên rồi chia thành 120 mẫu train, 40 mẫu validation và 40 mẫu test.
2. Dòng 18–24 bọc dữ liệu train bằng `TensorDataset` và `DataLoader` với `batch_size=32`, `shuffle=True`, `num_workers=0` cùng `torch.Generator` đã đặt seed.
3. Dòng 38–42 định nghĩa hàm `eval_accuracy`, trong đó gọi `model.eval()` và bọc suy luận trong `with torch.no_grad():`.
4. Dòng 49–56 train 20 epoch, bật lại `model.train()` ở đầu mỗi epoch trước khi lặp qua các batch và in tỉ lệ đoán đúng trên validation mỗi 5 epoch.
5. Dòng 58 tính `test_acc` đúng một lần sau khi kết thúc huấn luyện.

**Lưu ý:** Gọi `model.train()` ở đầu mỗi epoch đưa mô hình trở lại chế độ huấn luyện sau khi `eval_accuracy` đã chuyển sang `model.eval()`.

**Thử tự sửa:** Đổi `batch_size=32` thành `batch_size=16` để mỗi epoch có nhiều bước cập nhật trọng số hơn, rồi so sánh tỉ lệ đoán đúng trên validation tại epoch 5.
