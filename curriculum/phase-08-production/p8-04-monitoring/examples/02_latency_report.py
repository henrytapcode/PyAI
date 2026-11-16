# Latency percentile report (min, mean, p50, p90, p95, max) and top 3 slowest calls.

import math
import statistics


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    rank = math.ceil(p / 100 * len(ordered))
    return ordered[rank - 1]


def main() -> None:
    samples = [
        ("req-01", 180),
        ("req-02", 210),
        ("req-03", 195),
        ("req-04", 240),
        ("req-05", 1420),
        ("req-06", 205),
        ("req-07", 190),
        ("req-08", 225),
        ("req-09", 215),
        ("req-10", 880),
        ("req-11", 200),
        ("req-12", 185),
        ("req-13", 230),
        ("req-14", 2650),
        ("req-15", 195),
        ("req-16", 220),
        ("req-17", 250),
        ("req-18", 205),
        ("req-19", 940),
        ("req-20", 215),
    ]

    latencies = [ms for _, ms in samples]
    rows = [
        ("min", min(latencies)),
        ("mean", round(statistics.mean(latencies), 1)),
        ("p50", percentile(latencies, 50)),
        ("p90", percentile(latencies, 90)),
        ("p95", percentile(latencies, 95)),
        ("max", max(latencies)),
    ]

    print("metric | value")
    print("-------|------")
    for name, val in rows:
        print(f"{name:<6} | {val}")

    slowest = sorted(samples, key=lambda item: item[1], reverse=True)[:3]
    print("\nslowest 3:")
    for req_id, ms in slowest:
        print(f"  {req_id}: {ms} ms")


if __name__ == "__main__":
    main()
