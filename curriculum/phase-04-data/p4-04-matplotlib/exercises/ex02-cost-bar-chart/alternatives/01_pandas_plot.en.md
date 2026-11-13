# Plotting directly from a pandas Series

Instead of extracting `totals.index.tolist()` and `totals.tolist()` for `ax.bar(...)`, this version calls `totals.plot(kind="bar", ax=ax)` directly on the aggregated pandas `Series`. It is shorter for quick exploratory charts and automatically sets the x-axis label to the grouped column name (`"model"`), whereas calling `ax.bar(...)` directly gives you explicit control over bar styling and leaves tick labels horizontal by default.
