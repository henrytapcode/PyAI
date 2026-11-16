# Three-day monitoring summary with early budget warning at 85% spend.

import math


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    rank = math.ceil(p / 100 * len(ordered))
    return ordered[rank - 1]


def summarize(records: list[dict]) -> dict:
    count = len(records)
    latencies = [r["latency_ms"] for r in records]
    errors = sum(1 for r in records if r["status"] != "ok")
    hits = sum(1 for r in records if r["cache_hit"])
    total_cost = sum(r["cost_usd"] for r in records)
    return {
        "count": count,
        "error_rate": round(errors / count, 4),
        "p95_ms": percentile(latencies, 95),
        "total_cost": round(total_cost, 2),
        "cache_hit_rate": round(hits / count, 2),
    }


def check_alerts(summary: dict, max_p95_ms: float, budget: float, max_error_rate: float) -> list[str]:
    alerts: list[str] = []
    if summary["p95_ms"] > max_p95_ms:
        alerts.append(f"p95 latency {summary['p95_ms']}ms > {max_p95_ms}ms")
    ratio = summary["total_cost"] / budget
    if summary["total_cost"] > budget:
        alerts.append(f"budget exceeded: ${summary['total_cost']:.2f} > ${budget:.2f}")
    elif ratio >= 0.8:
        pct = round(ratio * 100)
        alerts.append(f"budget warning: {pct}% of budget used (${summary['total_cost']:.2f}/${budget:.2f})")
    if summary["error_rate"] > max_error_rate:
        alerts.append(f"error rate {summary['error_rate']:.2f} > {max_error_rate:.2f}")
    return alerts


def main() -> None:
    days = {
        "day_1": [
            {"latency_ms": 210, "cost_usd": 2.10, "cache_hit": True, "status": "ok"},
            {"latency_ms": 240, "cost_usd": 3.40, "cache_hit": False, "status": "ok"},
            {"latency_ms": 195, "cost_usd": 1.80, "cache_hit": True, "status": "ok"},
            {"latency_ms": 310, "cost_usd": 4.20, "cache_hit": False, "status": "ok"},
        ],
        "day_2": [
            {"latency_ms": 220, "cost_usd": 6.50, "cache_hit": False, "status": "ok"},
            {"latency_ms": 1650, "cost_usd": 14.00, "cache_hit": False, "status": "ok"},
            {"latency_ms": 290, "cost_usd": 8.00, "cache_hit": False, "status": "error"},
            {"latency_ms": 260, "cost_usd": 5.50, "cache_hit": False, "status": "ok"},
        ],
        "day_3": [
            {"latency_ms": 230, "cost_usd": 4.25, "cache_hit": True, "status": "ok"},
            {"latency_ms": 280, "cost_usd": 5.10, "cache_hit": False, "status": "ok"},
            {"latency_ms": 260, "cost_usd": 4.00, "cache_hit": True, "status": "ok"},
            {"latency_ms": 310, "cost_usd": 3.65, "cache_hit": False, "status": "ok"},
        ],
    }

    for day, records in days.items():
        summary = summarize(records)
        alerts = check_alerts(summary, max_p95_ms=1000, budget=20.0, max_error_rate=0.05)
        print(
            f"{day}: count={summary['count']} p95={summary['p95_ms']}ms "
            f"cost=${summary['total_cost']:.2f} hit_rate={summary['cache_hit_rate']:.2f}"
        )
        print("  alerts:", alerts if alerts else "none")


if __name__ == "__main__":
    main()
