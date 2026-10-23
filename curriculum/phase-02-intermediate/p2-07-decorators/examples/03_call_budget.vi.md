# Ngân sách số lần gọi cho một LLM

**Ví dụ này cho thấy:** một decorator có tham số. `@limit_calls(2)` cho phép hàm chạy hai lần rồi từ chối, giúp bạn tránh một vòng lặp lỡ tay làm tốn tiền.

**Từng bước**
1. Dòng 5–16 có ba tầng: `limit_calls(max_calls)` trả về `decorator`, và `decorator` trả về `wrapper`.
2. Dòng 7 tạo list `used` một lần cho mỗi hàm được decorate. Mỗi lần gọi được cho phép thêm một phần tử vào đó, nên `len(used)` là số lần đã gọi.
3. Dòng 11–12 kiểm tra ngân sách **trước** khi gọi hàm, và `raise` một `RuntimeError` khi đã dùng hết.
4. Dòng 19–21 decorate `ask_llm`, một stub trả về văn bản cố định thay vì gọi API thật.
5. Dòng 24–25 dùng hết ngân sách. Dòng 26–29 thử lần thứ ba và bắt lỗi bằng `try` / `except`.

**Để ý:** dòng 19 có ngoặc: `@limit_calls(2)`. Số `2` là thiết lập, và nó đi trong ba lô của `wrapper` với tên `max_calls`.

**Tự thử:** đổi `@limit_calls(2)` thành `@limit_calls(3)`. Lần gọi thứ ba bây giờ phải thành công và không có gì bị chặn.
