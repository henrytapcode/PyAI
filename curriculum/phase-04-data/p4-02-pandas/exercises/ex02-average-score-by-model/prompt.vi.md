Viết hàm `average_score_by_model(df)` để tính điểm eval trung bình cho từng mô hình trên các lượt chạy thành công (`status == "ok"`). Hãy viết code bên trong hàm và `return` kết quả dưới dạng `dict[str, float]` của Python.

**Ví dụ**

```python
df = pd.DataFrame({
    "model": ["gpt-4o", "gpt-4o", "claude", "llama"],
    "status": ["ok", "ok", "error", "ok"],
    "score": [0.90, 0.96, 0.0, 0.80],
})
average_score_by_model(df)
# -> {"gpt-4o": 0.93, "llama": 0.8}
```

**Quy tắc**
- Chỉ giữ các hàng có `status == "ok"`. Mô hình không có hàng `"ok"` nào thì không được xuất hiện trong dictionary trả về.
- Làm tròn mỗi điểm trung bình tới 2 chữ số thập phân.
- Trả về `dict` Python thuần với giá trị là kiểu `float` thuần của Python (không phải `np.float64`).
- Trả về `{}` khi không có hàng nào `status == "ok"` (hoặc khi `df` rỗng).
- Không làm thay đổi `df` đầu vào.
