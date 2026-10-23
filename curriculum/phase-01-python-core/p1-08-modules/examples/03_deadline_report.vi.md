# Deadline, đường dẫn và `__main__` guard

**Ví dụ này cho thấy:** tính toán ngày tháng với `datetime`, cái nhìn đầu tiên về `pathlib`, và mẫu `if __name__ == "__main__":` có mặt trong gần như mọi script thật.

**Từng bước**
1. Dòng 2–3 import tên bằng `from ... import ...`: `date` và `timedelta` từ `datetime`, `Path` từ `pathlib`.
2. Dòng 6–7: trừ hai ngày cho ra một `timedelta`; `.days` của nó là một số nguyên bình thường.
3. Dòng 10–12: `Path("data/raw/reviews.csv")` hiểu đây là một đường dẫn file. `.stem` là tên không có đuôi, `.suffix` là phần đuôi, `.parts` là tuple các thành phần của đường dẫn. Không có gì được đọc từ ổ đĩa: nó chỉ xử lý chuỗi đường dẫn.
4. Dòng 15–23 là `main()`. Dòng 17 cộng `timedelta(days=45)` vào một ngày: 1/3 cộng 45 ngày là 15/4. Dòng 20 đổi ngày thành tên thứ trong tuần (`%A` nghĩa là "tên đầy đủ của thứ"). Dòng 22 nối các phần đường dẫn bằng `/`.
5. Dòng 26–27: `__name__` chỉ bằng `"__main__"` khi đây là file bạn chạy. Nếu file khác `import` nó, `main()` sẽ **không** chạy, các hàm chỉ đơn giản trở nên dùng được.

**Để ý:** các hàm ở trên làm việc và trả về giá trị; `main()` lo việc in. Cách tách này giúp hàm dễ dùng lại và dễ test.

**Tự thử:** đổi ngày bắt đầu hoặc con số `45`, và đoán deadline mới trước khi chạy.
