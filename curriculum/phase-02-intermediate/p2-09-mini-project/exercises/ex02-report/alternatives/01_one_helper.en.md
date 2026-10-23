# One helper, two key functions

The two totals functions repeat the same loop, and only the key changes. This version writes the loop once in `group_totals` and passes the "how to get the key" as a function (functions are values). `max(totals, key=totals.get)` is a built-in way to find the best key: it calls `totals.get` on every key and returns the key with the biggest result. Because the keys are already sorted, `max` returns the first of equal totals, so ties still go to the earlier name.

This is the better design when you expect more groupings later (by note, by week). For three small functions, the plain loops of the main solution are easier to read for a beginner.
