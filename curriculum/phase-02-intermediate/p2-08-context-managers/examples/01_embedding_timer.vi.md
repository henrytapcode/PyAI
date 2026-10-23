# Timer cho embedding

**Ví dụ này cho thấy:** một timer viết bằng `@contextmanager`, ghi lại mỗi lần gọi embedding giả mất bao lâu, kể cả khi lần gọi đó bị lỗi. Đồng hồ là một tham số nên các con số luôn giống nhau.

**Từng bước**
1. Dòng 4–8 tạo một đồng hồ giả. Mỗi lần gọi nó trả về số kế tiếp trong `ticks`, nên không dùng thời gian thật.
2. Dòng 11–17 định nghĩa `timer`. Nó đọc đồng hồ, nhường chỗ cho phần thân qua `yield`, và trong `finally` lưu nhãn cùng thời gian đã trôi vào `results`.
3. Dòng 26–32 đo hai lần gọi thành công. Mỗi `with` đọc đồng hồ hai lần.
4. Dòng 34–38 đo một lần gọi bị lỗi: `len(None)` raise `TypeError`. Thời gian vẫn được lưu, rồi lỗi mới đến `except`.
5. Dòng 40–41 in ra mọi thời gian đã lưu.

**Để ý:** `broken batch: 0.2s` vẫn xuất hiện trong danh sách cuối dù lần gọi đó thất bại. Đó là tác dụng của `try/finally` quanh `yield`.

**Tự thử:** xóa các dòng `try:` và `finally:` trong `timer` (và bỏ phần thụt lề thêm). Chạy lại: lần gọi lỗi không còn được ghi.
