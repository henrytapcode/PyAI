# Prompt tokens vs. latency scatter plot

**What it shows:** plotting individual `(tokens, latency_ms)` measurements with `ax.scatter()` to inspect their relationship, and printing their correlation coefficient.

**Step by step**
1. Lines 5–6 define NumPy arrays of prompt token counts and response latencies for 8 requests.
2. Lines 8–14 create `(fig, ax)`, draw a scatter plot with `ax.scatter(tokens, latency_ms)`, label the axes, enable gridlines, and call `plt.show()`.
3. Lines 16–17 compute the Pearson correlation with `np.corrcoef(...)`, cast to `float`, round to two decimals, and print it.

**Notice:** `ax.scatter` plots disconnected dots instead of joining them with segments, which is what you want when `x` values are independent measurements.

**Try it yourself:** change the last `latency_ms` entry `790` to `250` (simulating a cached fast response) and see how the scatter plot and correlation change.
