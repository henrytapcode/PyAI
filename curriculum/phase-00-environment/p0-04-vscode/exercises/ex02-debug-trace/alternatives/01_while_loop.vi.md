# Dùng vòng lặp while tường minh

Cách làm này thay `enumerate()` bằng biến đếm chỉ số `idx` và vòng lặp `while`, đồng thời `return` ngay khi `hit` là `True`. Trong Python, `for ... in enumerate(...)` được ưa chuộng hơn vì bạn không thể quên `idx += 1`, còn bản `while` thể hiện rõ từng bước tăng chỉ số giống cách debugger bước qua vòng lặp.
