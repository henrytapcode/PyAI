# Functional pipeline with `collections.Counter` and pure helpers

This alternative decomposes span construction (`_build_span`), nearest-rank percentile computation (`_nearest_rank_p95`), and line clamping (`_clamp_line`) into small pure functions, and uses `collections.Counter` with generator expressions in `summarize_traces`. Compared to the single-pass `for` loop in `solution.py`, this style is more declarative and concise, at the trade-off of iterating over `spans` multiple times (still `O(N)` overall, negligible for typical agent trace batches).
