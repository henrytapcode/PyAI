# Cleaning classifier training labels

**What it shows:** normalising text and labels with `.str` methods, dropping empty texts, deduplicating repeated samples, and checking the final label distribution with `value_counts()`.

**Step by step**
1. Lines 4–23 create a small `(text, label)` dataset with extra spaces, mixed case, `_` and `-` separators, blank texts, and a repeated prompt.
2. Lines 25–33 copy the table, strip outer whitespace from `text`, and normalise `label` by stripping, lowercasing, and replacing `_` and `-` with spaces.
3. Lines 35–36 remove blank `text` rows and drop duplicate `text` entries while keeping the latest row (`keep="last"`).
4. Lines 38–41 print the cleaned dataset and the final `value_counts()` per label.

**Notice:** stripping `text` before checking `df["text"] != ""` and deduplicating catches `"   "` as blank and merges `" Reset password "` with `"Reset password"`.

**Try it yourself:** change `keep="last"` on line 36 to `keep="first"` and see how the row order of `Reset password` changes.
