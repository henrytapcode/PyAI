# Chia lô cho embedding

**Ví dụ này cho thấy:** một bước chuẩn bị rất điển hình trong AI. Làm sạch tài liệu theo kiểu lười, rồi gửi cho embedding model theo từng lô nhỏ. Ở đây một lô bị giới hạn bởi tổng số ký tự, không phải bởi một số phần tử cố định.

**Từng bước**
1. Dòng 2–13 định nghĩa `batches_by_budget`. Nó giữ một list nhỏ tên `batch` và một biến đếm `used` ghi số ký tự đã gom được.
2. Dòng 6–9 chạy trước khi thêm một văn bản: nếu thêm nó sẽ làm `used` vượt quá `max_chars`, lô hiện tại được yield và một lô rỗng mới bắt đầu.
3. Dòng 10–11 thêm văn bản vào lô và cập nhật `used`. Dòng 12–13 yield lô còn dư ở cuối.
4. Dòng 16–17 là một lời gọi embedding giả. Hàm thật sẽ trả về các vector, ở đây nó chỉ trả về độ dài của chuỗi.
5. Dòng 32–33 là hai generator expression: strip từng tài liệu, rồi bỏ các tài liệu rỗng.
6. Dòng 36–39 lặp qua các lô và in một dòng cho mỗi lần gọi, kèm độ dài từng văn bản và tổng của chúng.

**Lưu ý:** các lô có kích thước khác nhau (2, 2 và 3 văn bản) vì văn bản ngắn xếp vừa nhau còn văn bản dài thì không. Phần `batch and` ở dòng 6 giúp tránh yield một lô rỗng khi văn bản đầu tiên đã dài sẵn.

**Thử tự làm:** đổi số `30` ở dòng 36 thành `20`. Mỗi lần gọi giờ chứa ít văn bản hơn, và bạn sẽ thấy sáu lần gọi.
