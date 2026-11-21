def find_first_above(values: list[float], threshold: float) -> int | None:
    for i, value in enumerate(values):
        if value >= threshold:
            return i + 1
    return -1


def trace_watch(values: list[int], breakpoint_val: int) -> list[dict]:
    steps: list[dict] = []
    running_sum = 0
    for i, v in enumerate(values):
        if v == breakpoint_val:
            break
        running_sum = v
        steps.append(
            {
                "index": i,
                "value": v,
                "running_sum": running_sum,
                "hit_breakpoint": v == breakpoint_val,
            }
        )
    return steps
