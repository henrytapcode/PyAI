Điền vào các ô `___` trong hàm `plot_loss(epochs, losses)` để vẽ biểu đồ đường thể hiện training loss qua các epoch và trả về `(fig, ax)`. Viết code bên trong hàm và `return` cặp `(fig, ax)`, không gọi `plt.show()`.

**Ví dụ**

```python
fig, ax = plot_loss([1, 2, 3], [0.9, 0.5, 0.3])
ax.get_title()    # "Training loss"
ax.get_xlabel()   # "epoch"
ax.get_ylabel()   # "loss"
```

**Quy tắc**

- Tạo biểu đồ bằng `plt.subplots()`.
- Vẽ `epochs` theo `losses` với `label="loss"` và `marker="o"`.
- Đặt tiêu đề `"Training loss"`, nhãn trục x `"epoch"` và nhãn trục y `"loss"`.
- Bật hộp chú thích bằng `ax.legend()`.
- Không gọi `plt.show()` bên trong `plot_loss`.
