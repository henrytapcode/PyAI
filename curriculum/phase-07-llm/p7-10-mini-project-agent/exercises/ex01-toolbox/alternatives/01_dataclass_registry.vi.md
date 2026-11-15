# Registry một dictionary kèm dataclass

Cách tiếp cận này gom hàm thực thi, bản sao schema và cờ `side_effect` vào một dataclass `_ToolEntry` bất biến trong duy nhất một dictionary `_entries` giữ thứ tự chèn, đồng thời tách bước kiểm tra tham số sang `_prepare_args()`. Vì `dict` của Python giữ nguyên thứ tự thêm vào, ta không cần một danh sách `_order` riêng và tránh được lệch đồng bộ giữa nhiều cấu trúc lưu trữ khi mở rộng.
