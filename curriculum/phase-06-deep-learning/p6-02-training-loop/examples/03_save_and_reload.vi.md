# Lưu và nạp lại state_dict của model

**Điều cần thấy:** Train nhanh một model, lưu `state_dict` vào `tempfile.TemporaryDirectory()`, nạp trọng số đó vào một `TinyNet` mới với `weights_only=True`, rồi kiểm tra hai model cho kết quả giống hệt nhau.

**Từng bước**
1. Dòng 7–33 tạo 120 điểm 2D tổng hợp và train `TinyNet` trong 20 epoch.
2. Dòng 35–38 tính dự đoán `pred_a` và accuracy `acc_a` của model gốc dưới `model.eval()` và `torch.no_grad()`.
3. Dòng 40–42 lưu `model.state_dict()` ra file tạm (`tinynet.pt`), thư mục tạm sẽ tự động được dọn sạch khi thoát khối `with`.
4. Dòng 44–49 tạo một `TinyNet()` hoàn toàn mới, nạp tham số đã lưu bằng `torch.load(path, weights_only=True)`, rồi tính `pred_b` và `acc_b` ở chế độ `eval()`.
5. Dòng 51–53 in hai giá trị accuracy và kết quả `torch.equal(pred_a, pred_b)` (`True`).

**Lưu ý:** `state_dict()` chỉ lưu các tensor tham số (trọng số và bias), không lưu code của class `TinyNet`, nên bạn luôn phải khởi tạo `TinyNet()` trước rồi mới gọi `load_state_dict(...)`. Ở đây ta đo accuracy trên `X_train` chỉ để đối chiếu model gốc với model nạp lại; muốn biết model tốt đến đâu thì vẫn phải dùng tập validation và test.

**Thử tự sửa:** Tạm comment dòng `reloaded.load_state_dict(...)` trong một lần chạy để kiểm chứng rằng `TinyNet()` mới chưa nạp trọng số sẽ dự đoán khác đi (`same predictions: False`).
