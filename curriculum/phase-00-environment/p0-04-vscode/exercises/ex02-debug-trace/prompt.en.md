`starter.py` contains buggy implementations of two debugging helpers. Fix both functions so all tests pass:

1. `find_first_above(values: list[float], threshold: float) -> int | None`
   - Return the **0-based index** of the first element strictly greater than `threshold` (`value > threshold`).
   - Return `None` if no element is strictly greater than `threshold`.

2. `trace_watch(values: list[int], breakpoint_val: int) -> list[dict]`
   - Step through `values` from index `0`, maintaining `running_sum` (starting at `0`, adding each `v`).
   - For each element, record:
     ```python
     {
         "index": i,
         "value": v,
         "running_sum": running_sum,
         "hit_breakpoint": v == breakpoint_val,
     }
     ```
   - Stop immediately **after** recording the first step where `hit_breakpoint` is `True`.
