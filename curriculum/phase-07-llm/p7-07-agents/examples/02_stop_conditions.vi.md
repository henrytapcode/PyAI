# Bốn điều kiện dừng của agent

**Điểm nổi bật:** Một hàm `run_agent()` duy nhất dừng gọn gàng theo bốn lý do khác nhau—`final`, `max_steps`, `repeat` và `budget`—với bốn kịch bản `FakeLLM` khác nhau.

**Từng bước**
1. Dòng 33–60 cài đặt `run_agent()` với bốn lớp phanh: vòng `for` giới hạn bởi `max_steps`, cộng dồn `total_tokens` so với `token_budget`, trả lời sớm khi không còn `tool_calls`, và kiểm tra lặp so với `trace[-1]`.
2. Dòng 63–101 khai báo bốn kịch bản: hoàn thành bình thường sau 2 bước, gọi luân phiên hai tool vượt quá `max_steps=3`, gọi lặp lại đúng tool và tham số ở bước 2, và đặt `token_budget=25`.
3. Dòng 103–105 chạy từng kịch bản với một `FakeLLM(script=script)` mới rồi in `stopped_reason`, `steps` và `tokens`.

**Lưu ý:** Kiểm tra `token_budget` ngay sau `client.chat()` và kiểm tra `repeat` trước khi thực thi tool giúp không chạy thừa tool và giữ đúng số bước thực tế.

**Tự thử:** Tăng `token_budget` ở kịch bản thứ tư từ `25` lên `100` và kiểm tra `stopped_reason` chuyển từ `budget` sang `final`.
