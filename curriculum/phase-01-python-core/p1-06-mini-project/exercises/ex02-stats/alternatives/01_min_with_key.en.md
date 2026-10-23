# Built-in `min` with a key

This version first builds a list of rows (name and average), then lets the built-in `min(rows, key=...)` pick the winner. It uses the same trick as `sorted`: the key function returns a tuple, and the row with the smallest tuple wins. `best_key` flips the sign of the average, so the highest average gives the smallest key; `worst_key` does not flip it. Both put the name second, so ties go to the earlier name. `sum(row["avg"] for row in rows)` is a compact way to add the averages up (a preview of a later topic).

It is shorter and says clearly what it wants ("the minimum by this key"). The loop in the main solution is the better way to learn how "best so far" works, and it needs only one pass over the data.
