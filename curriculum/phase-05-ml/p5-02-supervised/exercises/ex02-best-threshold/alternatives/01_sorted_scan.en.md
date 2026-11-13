# Single-pass sorted scan

Instead of re-scanning the entire `scores` array for every candidate threshold (`O(n^2)` work), this version sorts `(score, label)` pairs once and sweeps through them from lowest to highest in pure Python loops (`O(n log n)`). At each distinct score `t`, `left_zeros + right_ones` gives the exact number of correct predictions without rebuilding prediction arrays every step. For tiny arrays of a dozen items the NumPy loop in `solution.py` is shorter and fast enough, while on tens of thousands of scores this sorted scan avoids quadratic work.
