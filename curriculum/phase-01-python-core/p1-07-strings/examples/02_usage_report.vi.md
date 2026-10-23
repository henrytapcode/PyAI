# Báo cáo sử dụng

**Ví dụ này cho thấy:** format spec trong f-string (`:<12`, `:>12,`, `:>14.4f`) dựng một bảng có các cột ngay ngắn.

**Từng bước**
1. Dòng 2–5 lưu mức sử dụng của từng model trong một dictionary lồng dictionary: mỗi tên model ứng với số token và giá mỗi triệu token.
2. Dòng 8 in tiêu đề. Tên cột là chuỗi, nên `'model':<12` căn trái trong 12 ký tự còn `'tokens':>12` căn phải trong 12.
3. Dòng 10–14 lặp qua các model. `cost` bằng `tokens / 1000000 * price`, còn `total` gom tổng, giống mẫu accumulator trong bài vòng lặp.
4. Dòng 14 in mỗi hàng với **cùng độ rộng như tiêu đề** (12, 12, 14), nhờ vậy các cột thẳng hàng. `:>12,` thêm dấu phẩy ngăn hàng nghìn và `:>14.4f` hiển thị 4 chữ số thập phân.
5. Dòng 16–17 vẽ một đường gồm 38 dấu gạch (12 + 12 + 14) và in tổng.

**Để ý:** format spec chỉ đổi cách một giá trị được *hiển thị*. Bên trong chương trình, `tokens` vẫn là số `1250000` bình thường.

**Tự thử:** đổi `:>14.4f` thành `:>14.2f` ở cả hai dòng và kiểm tra các cột vẫn thẳng hàng.
