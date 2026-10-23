# Comprehension và key để sắp xếp

Trước hết tìm các tên không trùng bằng set comprehension đã sắp xếp, rồi tính từng tổng bằng `sum(...)` trên một generator expression lọc ra một nhóm. Với danh mục lớn nhất, `sorted(totals, key=...)` sắp xếp các tên bằng key là tuple `(-total, name)`, giống hệt cách xếp hạng trong project bảng điểm, và lấy phần tử đầu. (`lambda name: ...` là một hàm một dòng rất nhỏ không có tên, một món xem trước của chủ đề sau.)

Cách này đọc dễ chịu và không cần accumulator, nhưng nó duyệt cả list một lần **cho mỗi nhóm**, nên chậm lại khi có nhiều nhóm. Vòng lặp một lượt của lời giải chính là lựa chọn tốt hơn cho list lớn.
