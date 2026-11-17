# Combined TTL and LRU cache timeline using an injected FakeClock.

from collections import OrderedDict


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


class TTLLRUCache:
    def __init__(self, maxsize: int, ttl: float, clock) -> None:
        self.maxsize = maxsize
        self.ttl = ttl
        self.clock = clock
        self.entries: OrderedDict[str, tuple[str, float]] = OrderedDict()

    def set(self, key: str, value: str) -> None:
        if key in self.entries:
            self.entries.move_to_end(key)
        self.entries[key] = (value, self.clock() + self.ttl)
        if len(self.entries) > self.maxsize:
            self.entries.popitem(last=False)

    def get(self, key: str) -> str:
        item = self.entries.get(key)
        if item is None:
            return "MISS"
        value, expires_at = item
        if self.clock() >= expires_at:
            del self.entries[key]
            return "EXPIRED"
        self.entries.move_to_end(key)
        return f"HIT({value})"


def main() -> None:
    clock = FakeClock(start=0.0)
    cache = TTLLRUCache(maxsize=3, ttl=30.0, clock=clock)

    timeline = [
        (0, "set", "k1", "v1"),
        (5, "set", "k2", "v2"),
        (10, "set", "k3", "v3"),
        (12, "get", "k1", ""),
        (15, "set", "k4", "v4"),
        (20, "get", "k2", ""),
        (36, "get", "k3", ""),
        (40, "get", "k1", ""),
        (42, "get", "k4", ""),
    ]

    print("t  | op  | key | result  | keys in cache")
    print("---+-----+-----+---------+--------------------")
    for target_t, op, key, val in timeline:
        if target_t > clock():
            clock.advance(target_t - clock())
        if op == "set":
            cache.set(key, val)
            res = "STORED"
        else:
            res = cache.get(key)
        keys = list(cache.entries.keys())
        print(f"{target_t:<2} | {op:<3} | {key:<3} | {res:<7} | {keys}")


if __name__ == "__main__":
    main()
