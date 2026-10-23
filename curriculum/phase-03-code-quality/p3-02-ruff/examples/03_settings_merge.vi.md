# Settings không dùng chung trạng thái

**Ví dụ này cho thấy:** mẫu tham số mặc định an toàn trong một việc thực tế: tạo setting cho model từ giá trị mặc định cộng với các giá trị ghi đè tùy chọn.

**Từng bước**
1. Dòng 2 chứa các setting mặc định.
2. Dòng 5 cho `overrides` mặc định là `None`, không phải `{}`. Hint `dict[...] | None` cũng nói đúng điều đó.
3. Dòng 6 sao chép `DEFAULTS` bằng `dict(DEFAULTS)`, nên sửa bản sao không bao giờ đổi bản gốc.
4. Dòng 7–8 áp dụng các giá trị ghi đè bằng `update`, chỉ khi người gọi có truyền vào. `update` thêm hoặc thay các key trong dict.
5. Dòng 12–17 tạo hai bộ setting và cho thấy chúng tách biệt, còn `DEFAULTS` không bị đụng tới.

**Để ý:** nếu dòng 5 viết `overrides={}` và dòng 6 trả về chính dict đó, `B006` sẽ cảnh báo bạn. Lỗi này là thật: một lần gọi có thể làm đổi setting của mọi lần gọi sau.

**Tự thử:** đổi dòng 12 thành `build_settings({"model": "big"})`. Dòng 14 phải hiện `'model': 'big'`, còn dòng 15 vẫn hiện `'model': 'small'`.
