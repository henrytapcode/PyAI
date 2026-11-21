def find_first_above(values: list[float], threshold: float) -> int | None:
    idx = 0
    while idx < len(values):
        if values[idx] > threshold:
            return idx
        idx += 1
    return None


def trace_watch(values: list[int], breakpoint_val: int) -> list[dict]:
    steps: list[dict] = []
    running_sum = 0
    idx = 0
    while idx < len(values):
        v = values[idx]
        running_sum += v
        hit = v == breakpoint_val
        steps.append(
            {
                "index": idx,
                "value": v,
                "running_sum": running_sum,
                "hit_breakpoint": hit,
            }
        )
        if hit:
            return steps
        idx += 1
    return steps
