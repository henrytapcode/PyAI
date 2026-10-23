# Làm sạch trước, loại trùng sau

Phiên bản này chia việc thành hai lượt. Vòng lặp chỉ bỏ qua, làm sạch và đếm các văn bản rỗng. Sau đó `dict.fromkeys(cleaned_texts)` tạo một dictionary có key là các văn bản, và dictionary giữ mỗi key một lần theo thứ tự xuất hiện đầu tiên, nên `list(...)` của nó là list không còn trùng. Số lượng trùng đơn giản là số văn bản đã mất đi. Cách này ngắn và rõ, nhưng nó giữ mọi văn bản đã sạch trong bộ nhớ trước khi loại trùng. Set `seen` của lời giải chính quyết định từng mục một, là lựa chọn tốt hơn cho một dataset rất lớn.
