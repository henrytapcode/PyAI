# Importing the names directly

This version uses `from statistics import mean, median, stdev`, so the calls are shorter: `mean(values)` instead of `statistics.mean(values)`. It is a good choice when you use a few names many times. The price is that a reader no longer sees at a glance which module `mean` came from, so keep the import list short and at the top.
