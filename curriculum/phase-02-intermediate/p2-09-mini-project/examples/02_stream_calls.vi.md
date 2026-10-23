# Đọc luồng các lệnh gọi đắt tiền

**Ví dụ này cho thấy:** một generator đọc từng dòng **lazily** (khi cần), và một decorator ghi log mỗi lần parse. Kết hợp lại, chúng cho thấy một pipeline lazy làm rất ít việc khi bạn chỉ xin hai kết quả.

**Từng bước**
1. Dòng 5–12 định nghĩa `logged`. Wrapper gọi hàm gốc, in ra thứ nó nhận và trả về, rồi trả kết quả đi. `@wraps` giữ nguyên tên hàm.
2. Dòng 15–18 áp decorator lên `parse_line`, hàm đổi `"large,0.40"` thành `("large", 0.4)`.
3. Dòng 21–25 định nghĩa generator `expensive_calls`. Nó parse từng dòng một và chỉ `yield` những lệnh gọi có giá từ `limit` trở lên.
4. Dòng 30 tạo generator. Chưa có gì chạy cả, nên `nothing parsed yet` là đúng.
5. Dòng 32–33 xin hai kết quả bằng `next`. Mỗi `next` chỉ chạy tiếp vòng lặp tới `yield` kế tiếp.
6. Dòng 34 in tên hàm, thứ mà `@wraps` đã giữ là `parse_line`.

**Để ý:** dòng cuối `small,0.03` không bao giờ được parse. Một list comprehension sẽ parse cả năm dòng trước.

**Tự thử:** thêm `print("third:", next(stream))` ở cuối. Generator hết dòng và kết thúc bằng lỗi `StopIteration`. Sau đó hãy xóa dòng này đi.
