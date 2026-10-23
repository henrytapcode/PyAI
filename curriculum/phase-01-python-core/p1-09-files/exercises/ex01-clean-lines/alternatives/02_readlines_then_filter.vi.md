# readlines rồi mới lọc

`f.readlines()` trả về mọi dòng trong một list (vẫn còn `\n`). File đóng ngay sau khối `with`, còn việc làm sạch diễn ra sau đó trong một vòng lặp bình thường. Cách này tách việc đọc file và việc làm sạch ra, đôi khi dễ đọc hơn. Đổi lại, mọi dòng nằm hết trong bộ nhớ cùng lúc, nên chỉ dùng cho file nhỏ.
