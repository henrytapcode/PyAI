# Sensor readings

**What it shows:** computing summary statistics and using boolean masks to separate outliers from clean sensor data.

**Step by step**
1. Line 4 puts seven temperature readings (in Celsius) into a 1D NumPy array.
2. Lines 5–7 print the minimum, maximum, and overall mean using `.min()`, `.max()`, and `.mean()`.
3. Line 9 builds a mask with `|` (or) to catch readings outside `[10, 35]` and extracts the two outliers (`41.8` and `-5.0`).
4. Line 12 uses `&` (and) with parentheses around each comparison to keep only the five normal readings, then prints their count and clean mean.

**Notice:** each condition around `&` or `|` must sit inside parentheses `( ... )`, and filtering creates a new array without changing `temps_c`.

**Try it yourself:** change the lower limit `10` on lines 9 and 12 to `20`. `normal count` will drop from `5` to `4` and `clean mean` will rise from `22.26` to `22.98`.
