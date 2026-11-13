# Batch predictions

**What it shows:** turning a 2D table of model class probabilities into predicted labels and counting confident predictions.

**Step by step**
1. Lines 4–10 store three class names and a `(4, 3)` probability table (4 samples × 3 classes, each row summing to `1.0`).
2. Line 12 runs `probs.argmax(axis=1)` to pick the column index with the highest probability for each row (`[2, 0, 1, 0]`).
3. Line 14 converts those numeric indices into readable strings using a list comprehension over `labels`.
4. Lines 16–19 grab each row's top probability with `.max(axis=1)` and count how many are at least `0.8` using `(top_probs >= 0.8).sum()`.

**Notice:** passing `axis=1` tells both `argmax` and `max` to look across the columns of each row, producing one answer per sample.

**Try it yourself:** lower the confidence threshold `0.8` on line 19 to `0.7`. The confident count should jump from `2` to `3`.
