Hàm `train(model, xs, ys, lr, epochs)` chạy được không báo lỗi nhưng cho kết quả sai vì đang có **2 lỗi**. Hãy tìm và sửa cả hai lỗi bên trong hàm, rồi `return` danh sách loss qua từng epoch.

**Ví dụ**

```python
torch.manual_seed(0)
model = nn.Linear(1, 1)
xs = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
ys = 2.0 * xs + 1.0
losses = train(model, xs, ys, lr=0.05, epochs=30)
# len(losses) == 30, mọi phần tử là float Python, và losses[-1] < 0.05
```

**Quy tắc**

- Trả về một `list` Python có độ dài đúng bằng `epochs`.
- Mỗi phần tử phải là `float` chuẩn của Python được làm tròn 4 chữ số thập phân (`round(loss.item(), 4)`), không phải tensor.
- Tiếp tục dùng `nn.MSELoss()` và `torch.optim.SGD(model.parameters(), lr=lr)`.
- Không sửa đổi `xs` hay `ys` tại chỗ.
