# Tìm kiếm tài liệu

**Ví dụ này cho thấy:** hai dataclass phối hợp với nhau. `Document` chứa dữ liệu. `Hit` có `order=True`, nên một list các hit có thể sắp xếp mà không cần viết code so sánh nào.

**Từng bước**
1. Dòng 5–9 định nghĩa `Document`. List `tags` dùng `default_factory`, nên mỗi tài liệu có list riêng.
2. Dòng 12–15 định nghĩa `Hit` với `order=True`. Các hit so sánh theo `score` trước, và chỉ so sánh `doc_id` khi hai score bằng nhau.
3. Dòng 18–23 tạo bốn tài liệu. Chỉ `d1` có tags.
4. Dòng 29 đếm từ: `text.split()` tạo list các từ, và `.count(word)` cho biết `word` xuất hiện bao nhiêu lần trong list đó.
5. Dòng 30–31 chỉ giữ lại các tài liệu có score lớn hơn 0, dưới dạng object `Hit`.
6. Dòng 32 sắp xếp các hit. `reverse=True` đặt hit lớn nhất lên đầu, nên kết quả khớp nhất đứng đầu.

**Lưu ý:** `d1` và `d2` cùng được 1 điểm. Thế hòa được phân xử bằng `doc_id`, và với `reverse=True` thì `d2` đứng trước `d1`.

**Tự thử:** tìm `"pasta"` thay vì `"python"`. Chỉ `d3` khớp, nên chỉ có một hit được in ra.
