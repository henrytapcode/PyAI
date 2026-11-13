Viết hàm `cost_bar_chart(df)` để cộng tổng chi phí `cost` theo từng `model`, sắp xếp các mô hình theo tổng chi phí giảm dần, vẽ biểu đồ cột lên `ax` rồi trả về `(fig, ax)`. Viết code bên trong hàm và `return` cặp `(fig, ax)`, không gọi `plt.show()`.

**Ví dụ**

```python
df = pd.DataFrame({
    "model": ["mini", "gpt-4o", "mini", "claude"],
    "cost": [0.15, 4.25, 0.25, 2.95],
})
fig, ax = cost_bar_chart(df)
# Các cột từ trái sang phải: "gpt-4o" (4.25), "claude" (2.95), "mini" (0.40)
```

**Quy tắc**

- Mỗi `model` chỉ xuất hiện một lần trên biểu đồ (cộng gộp các hàng trùng tên).
- Sắp xếp các cột từ tổng chi phí cao nhất xuống thấp nhất.
- Đặt tiêu đề `"Cost by model"` và nhãn trục y `"cost (USD)"`.
- Không sửa trực tiếp DataFrame `df` đầu vào, và không gọi `plt.show()`.
