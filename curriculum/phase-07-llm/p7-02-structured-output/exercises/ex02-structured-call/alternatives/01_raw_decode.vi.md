# Dùng json.JSONDecoder().raw_decode

Cách này dùng `json.JSONDecoder().raw_decode(text, start)` bắt đầu từ dấu `{` đầu tiên thay vì cắt tới dấu `}` cuối cùng. Bộ giải mã tự dừng ngay khi kết thúc object JSON hợp lệ đầu tiên, nên ghi chú phía sau có chứa thêm `{` hoặc `}` (như `"Ghi chú: {xem FAQ}"`) không làm hỏng việc parse. Đây là lựa chọn tốt hơn khi model hay viết thêm lời bình luận sau khối JSON, dù vẫn giả định dấu `{` đầu tiên chính là điểm mở đầu của object cần lấy.
