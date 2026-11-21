def find_first_above(values: list[float], threshold: float) -> int | None:
    for i, value in enumerate(values):
        if value > threshold:
            return i
    return None


def trace_watch(values: list[int], breakpoint_val: int) -> list[dict]:
    steps: list[dict] = []
    running_sum = 0
    for i, v in enumerate(values):
        running_sum += v
        hit = v == breakpoint_val
        steps.append(
            {
                "index": i,
                "value": v,
                "running_sum": running_sum,
                "hit_breakpoint": hit,
            }
        )
        if hit:
            break
    return steps
