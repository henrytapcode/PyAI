Viết hàm `clean_ratings(df)` để làm sạch một DataFrame thô có cột `user` và `rating`. Hãy viết code bên trong hàm và `return` về `DataFrame` đã làm sạch.

**Ví dụ**

`df` đầu vào:

```text
   user  rating
0   An      " 4 "
1  binh    "five"
2  an       "5"
3  chi      "7"
```

`DataFrame` trả về:

```text
  user  rating
0   an       5
```

**Quy tắc**

- Chuẩn hóa cột `user` bằng `.strip()` và `.lower()`.
- Chuyển `rating` sang số bằng `pd.to_numeric(..., errors="coerce")`, rồi bỏ các dòng không đọc được (`""`, `None`, `"five"`) hoặc nằm ngoài khoảng `1` đến `5`.
- Nếu cùng một `user` xuất hiện nhiều lần (sau khi chuẩn hóa tên), chỉ giữ lại dòng hợp lệ **cuối cùng**.
- `DataFrame` trả về phải có thứ tự cột `["user", "rating"]`, cột `rating` có dtype `"int64"`, và index đánh lại từ `0`.
- Không sửa trực tiếp `df` đầu vào.
