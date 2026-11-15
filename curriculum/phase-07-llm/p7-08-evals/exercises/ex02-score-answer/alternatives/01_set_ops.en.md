# Set difference with `dict.fromkeys` and generator `sum`

Instead of accumulating `matched`, `citations`, and `unsupported` with explicit `for` loops, this version computes `facts` via a generator `sum(...)`, deduplicates `citations` with `dict.fromkeys(...)`, and finds `missing = set(ans_words) - ctx_set` before filtering `dict.fromkeys(ans_words)` to preserve order of first appearance without duplicates. Set operations keep the code concise and fast on large contexts, while `dict.fromkeys` guarantees deterministic ordering for both `citations` and `unsupported`.
