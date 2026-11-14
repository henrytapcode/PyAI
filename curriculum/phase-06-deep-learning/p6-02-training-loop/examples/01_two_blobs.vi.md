# Huấn luyện bộ phân loại trên hai đám điểm 2D

**Điều cần thấy:** Định nghĩa `TinyNet(nn.Module)` hai tầng rồi train bằng `SGD` toàn bộ dữ liệu (full-batch) và `CrossEntropyLoss` trong 30 epoch trên hai đám điểm 2D tổng hợp.

**Từng bước**
1. Dòng 5–10 cố định seed (`torch.manual_seed(0)`) và tạo 200 điểm 2D tổng hợp: 100 điểm quanh `(-1, -1)` gắn nhãn `0` và 100 điểm quanh `(1, 1)` gắn nhãn `1`.
2. Dòng 13–21 định nghĩa `TinyNet` gồm `nn.Linear(2, 8)`, `nn.ReLU()` và `nn.Linear(8, 2)`.
3. Dòng 24–26 khởi tạo `model`, `nn.CrossEntropyLoss()` và `torch.optim.SGD(model.parameters(), lr=0.2)`.
4. Dòng 28–35 chạy 30 epoch full-batch theo đúng năm dòng chuẩn (`model(X)` -> `loss_fn` -> `zero_grad` -> `backward` -> `step`), in loss đã làm tròn mỗi 10 epoch.
5. Dòng 37–41 chuyển sang `model.eval()` và `torch.no_grad()` để tính và in tỉ lệ đoán đúng (accuracy) cuối trên tập train.

**Lưu ý:** Gọi `optimizer.zero_grad()` ở mỗi epoch giúp gradient không bị cộng dồn giữa các epoch, nhờ vậy loss giảm đều từ `0.19` ở epoch 10 xuống `0.079` ở epoch 30.

**Thử tự sửa:** Tăng số epoch từ `30` lên `60` (hoặc thử `lr=0.4`) và xem loss giảm xuống thêm bao nhiêu ở epoch cuối.
