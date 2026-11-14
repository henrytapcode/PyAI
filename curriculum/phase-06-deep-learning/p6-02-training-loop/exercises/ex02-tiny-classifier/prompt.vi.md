Hãy cài đặt một bộ phân loại PyTorch nhỏ và hàm hỗ trợ đánh giá:

1. `TinyClassifier(in_features, hidden, classes)` kế thừa `nn.Module`, nối tuần tự `nn.Linear(in_features, hidden)` -> `nn.ReLU()` -> `nn.Linear(hidden, classes)` trong `forward(self, x)` để trả về logits thô có shape `(N, classes)`.
2. `accuracy(model, xs, ys)` chuyển model bằng `model.eval()`, chạy dự đoán trong `with torch.no_grad():`, và trả về tỉ lệ dự đoán đúng làm tròn 3 chữ số thập phân dưới dạng `float` Python.

Hãy viết code bên trong class và hàm, rồi `return` kết quả.

**Ví dụ**

```python
torch.manual_seed(0)
clf = TinyClassifier(in_features=2, hidden=8, classes=3)
logits = clf(torch.randn(5, 2))  # shape (5, 3)
acc = accuracy(clf, torch.randn(10, 2), torch.zeros(10, dtype=torch.int64))
```

**Quy tắc**

- Phải gọi `super().__init__()` bên trong `TinyClassifier.__init__`.
- `TinyClassifier.forward` phải trả về logits thô (không áp dụng softmax).
- `accuracy` phải gọi `model.eval()`, bọc phần suy đoán trong `with torch.no_grad():`, và trả về `float` chuẩn của Python nằm trong `[0.0, 1.0]`.
- Không sửa đổi `xs` hay `ys` tại chỗ.
