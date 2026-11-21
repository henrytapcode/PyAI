`starter.py` chứa hai hàm hỗ trợ debug đang bị lỗi. Hãy sửa cả hai hàm để toàn bộ test đều pass:

1. `find_first_above(values: list[float], threshold: float) -> int | None`
   - Trả về **chỉ số 0-based** của phần tử đầu tiên lớn hơn hẳn `threshold` (`value > threshold`).
   - Trả về `None` nếu không có phần tử nào lớn hơn hẳn `threshold`.

2. `trace_watch(values: list[int], breakpoint_val: int) -> list[dict]`
   - Duyệt qua `values` từ chỉ số `0`, duy trì `running_sum` (bắt đầu từ `0`, cộng thêm từng `v`).
   - Với mỗi phần tử, ghi lại:
     ```python
     {
         "index": i,
         "value": v,
         "running_sum": running_sum,
         "hit_breakpoint": v == breakpoint_val,
     }
     ```
   - Dừng ngay **sau khi** ghi nhận bước đầu tiên có `hit_breakpoint` là `True`.
