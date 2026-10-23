Hàm `average` bên dưới lẽ ra phải trả về trung bình cộng của một list số, nhưng báo cáo test đang đỏ. Hãy đọc các test thất bại, tìm lỗi trong code và sửa chúng. Có hai lỗi: một lỗi lộ ra với đầu vào bình thường, và một lỗi chỉ lộ ra với list rỗng. Hãy sửa code bên trong hàm.

Các test hiện trong báo cáo dưới code của bạn. Hãy bắt đầu từ test đỏ đầu tiên và đọc hai vế của phép so sánh.

**Ví dụ**

| lời gọi | kết quả |
|---|---|
| `average([1, 2, 3])` | `2.0` |
| `average([5])` | `5.0` |
| `average([])` | raise `ValueError` |

**Quy tắc**
- Trả về tổng của tất cả các số chia cho số lượng của chúng.
- Với list rỗng, `raise ValueError` thay vì chia cho không.
- Không thay đổi list nhận vào.
