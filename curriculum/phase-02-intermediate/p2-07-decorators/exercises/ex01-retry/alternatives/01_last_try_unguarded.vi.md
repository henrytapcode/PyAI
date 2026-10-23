# Để lần thử cuối không có try

Vòng lặp chỉ xử lý `times - 1` lần thử đầu và nuốt lỗi của chúng bằng `pass`. Lần thử cuối là một lời gọi bình thường nằm ngoài `try`, nên nếu nó lỗi thì lỗi tự bay ra và bạn không cần lưu lại. Cách này ngắn hơn và tránh được `last_error`, nhưng nó dựa vào việc `times` ít nhất là 1, và quy tắc "bỏ cuộc" bị giấu ở dòng cuối, nên phiên bản `for ... try` dễ đọc hơn.
