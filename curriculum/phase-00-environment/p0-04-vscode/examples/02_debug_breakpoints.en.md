# Stepping through a boundary bug

**What it shows:** how a Watch-panel trace (`idx`, `score`, and `score > passing`) exposes an off-by-boundary comparison bug.

**Step by step**
1. `buggy_first_passing` checks `score > passing` instead of `score >= passing`.
2. When `score` is `70` and `passing` is `70`, the watch line prints `check=False`, so the loop skips index `1` and returns `2` (`88`) instead.
3. `fixed_first_passing` uses `>=`, returning index `1` as expected.

**Try it yourself:** change `passing` to `90` and run again to see both functions return `None`.
