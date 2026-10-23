# Cache cho các văn bản lặp lại

**Ví dụ này cho thấy:** một decorator nhớ các kết quả trước đó, để cùng một văn bản không bao giờ bị embed hai lần.

**Từng bước**
1. Dòng 6 tạo dict `saved` **bên trong** `cache_results`. Nó nằm trong closure, nên mỗi hàm được decorate có dict riêng của nó.
2. Dòng 9–13 định nghĩa wrapper. Nếu các đối số `args` (một tuple) chưa là key trong `saved`, nó gọi hàm thật và lưu kết quả. Sau đó nó trả về giá trị đã lưu.
3. Dòng 16 tạo list `calls`, ghi lại mỗi lần `embed_text` thật sự chạy.
4. Dòng 19–22 decorate `embed_text` bằng một phép embedding giả: `[độ dài, số chữ "a"]`.
5. Dòng 25–27 xin `"banana"` hai lần và `"kiwi"` một lần. Dòng 28–29 cho thấy hàm thật chỉ chạy hai lần.

**Để ý:** `"banana"` lần thứ hai trả về cùng list mà không chạy `embed_text`. Wrapper này chỉ nhận đối số vị trí (`*args`), vì key của dict phải là giá trị không thể thay đổi (immutable), mà `kwargs` là một dict nên không thể làm key.

**Tự thử:** thêm `print(embed_text("kiwi"))` trước dòng 28. Số lần gọi thật phải vẫn là 2.
