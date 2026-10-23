# Dùng `return` sớm thay cho `elif`

Mỗi quy tắc là một `if` riêng và trả về ngay, còn dòng cuối xử lý "những người còn lại". Logic giống hệt chuỗi `elif`: khi một quy tắc khớp, `return` kết thúc hàm nên các quy tắc phía sau không bao giờ được kiểm tra. Nhiều người thấy cách này phẳng và dễ đọc hơn.
