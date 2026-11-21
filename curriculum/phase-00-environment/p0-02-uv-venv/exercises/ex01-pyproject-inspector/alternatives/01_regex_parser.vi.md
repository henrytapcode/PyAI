# Biểu thức chính quy & hiệu tập hợp

Thay vì duyệt vòng lặp qua từng toán tử, phiên bản này dùng một biểu thức chính quy biên dịch sẵn (`re.compile`) để tách tên gói, phần `[extras]` tùy chọn, toán tử và phiên bản trong một bước, và dùng phép hiệu tập hợp (`req_set - inst_set`) trong `missing_packages`. Cả hai cách đều cho kết quả giống nhau; cách dùng vòng lặp dễ đọc hơn với người mới, còn cách dùng regex thuận tiện khi mở rộng thêm cú pháp PEP 508 sau này.
