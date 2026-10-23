# Dừng sớm bên trong vòng lặp

Thay vì cắt lát, hãy đi qua từng từ và thêm vào `kept` lần lượt. Ngay khi `kept` đã có đủ `limit` từ mà vẫn còn một từ nữa tới, tức là văn bản dài hơn mức cho phép, nên trả về những gì đang có cộng với `"..."`. Nếu vòng lặp kết thúc mà điều đó không xảy ra, nghĩa là mọi thứ đều vừa. Cách này dài hơn bản cắt lát, nhưng ý tưởng "dừng ngay khi quá dài" hữu ích khi đầu vào rất lớn hoặc đến từng phần một.
