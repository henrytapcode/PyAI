# A cost report with a safe ledger

**What it shows:** a small context manager, `ledger`, that loads the saved rows, lets you change them, and saves them again when the block ends. Then one grouping function builds two summaries, and a "best so far" loop finds the top model, with a tie to think about.

**Step by step**
1. Lines 12–16 define `ledger`. Setup: load the rows, or start with an empty list if the file does not exist. Then `yield rows`. After the block: save.
2. Lines 30–36 add rows in two separate sessions. The second session sees the rows of the first.
3. Lines 38–43 add a third row and then crash. The `path.write_text(...)` line after `yield` is skipped, so the file does not change.
4. Lines 19–24 define `cost_by`. It adds up `cost` for each value of `field`, and returns a dict with sorted keys and rounded totals.
5. Lines 47–50 print one summary by `model` and one by `day`, with exactly 4 decimals.
6. Lines 52–61 find the most expensive model with the "best so far" loop. Here `large` and `mid` have the same total, so the program also prints who is tied.

**Notice:** there is **no** `try/finally` around `yield` in `ledger`, and that is on purpose. A clean-up must always run, but saving half-finished work must not. When the block fails, we want to skip the save. Also notice `>=` in the last loop: with a tie, the later name (`mid`) replaces `large`.

**Try it yourself:** change `"cost": 9.99` to `0.5` and remove the `raise` line. Predict the new `rows saved` count (5). Then change `>=` to `>` in the last loop and predict who wins the tie (`large`).
