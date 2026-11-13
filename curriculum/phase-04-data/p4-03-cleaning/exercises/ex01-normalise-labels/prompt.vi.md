Điền vào các chỗ trống `___` bên trong hàm `normalise_labels(labels)` để làm sạch một pandas `Series` chứa nhãn lộn xộn: cắt khoảng trắng hai đầu, chuyển sang chữ thường, và thay cả `"_"` lẫn `"-"` bằng một dấu cách `" "`. Viết code bên trong hàm và `return` về `Series` đã làm sạch.

**Ví dụ**

```python
s = pd.Series([" Bug_Report ", "FEATURE-REQ", "  gpt_4o "])
normalise_labels(s).tolist()  # ["bug report", "feature req", "gpt 4o"]
```

**Quy tắc**

- Giữ nguyên index hàng ban đầu của `labels`.
- Không sửa trực tiếp `Series` đầu vào.
- Trả về một pandas `Series` (không phải `list` Python).
