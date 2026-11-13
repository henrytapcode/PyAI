# Picking a spam threshold

**What it shows:** Evaluating five candidate threshold values on 12 labelled support tickets and selecting the threshold with the best accuracy.

**Step by step**
1. Lines 4–5 define `scores` (spam probability estimates) and `labels` (`0` for normal, `1` for spam) for 12 tickets.
2. Lines 7–8 initialise `best_t` and `best_acc` to track the winning threshold.
3. Lines 10–16 loop through five candidate thresholds, turn `scores >= t` into `0`/`1` predictions with `.astype("int64")`, compute accuracy, and update the best result whenever accuracy improves.
4. Line 18 prints the winning threshold and its rounded accuracy.

**Notice:** One ticket has `score = 0.34` and `label = 1`, so `threshold = 0.55` still misses that outlier (`11 / 12 = 0.917`) — real datasets rarely separate at `1.0`.

**Try it yourself:** Add `0.34` to the candidate threshold list and check whether lowering the cutoff improves or hurts accuracy overall.
