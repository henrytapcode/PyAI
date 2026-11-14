# Vòng lặp theo mốc chỉ số và Counter

Thay vì cắt danh sách chỉ số đã xáo thành ba đoạn bằng slice rồi dùng list comprehension, cách này duyệt một lượt qua `enumerate(perm)` và rẽ từng cặp `(text, label)` theo mốc vị trí (`pos < n_train` hay `pos < n_train + n_val`), đồng thời dùng `collections.Counter` cho `class_counts`.

Cách viết một vòng lặp giúp nhìn rõ ranh giới từng tập và tránh tạo thêm các list chỉ số trung gian, còn list comprehension trên slice ở `solution.py` thì ngắn gọn hơn khi bạn đã quen với slicing trong Python.
