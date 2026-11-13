# Row-by-row loop

This version iterates over `probs` one row at a time, calls `row.argmax()` to get the best class index, and checks `row[best_idx]` directly instead of computing a separate `max(axis=1)` array. It is easy to read and works well if you need extra per-row logging or custom tie-breaking, though `argmax(axis=1)` plus `max(axis=1)` is faster when a batch has thousands of rows.
