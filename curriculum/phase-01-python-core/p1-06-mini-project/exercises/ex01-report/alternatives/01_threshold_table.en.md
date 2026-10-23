# A lookup table for letter grades

Instead of four `if` lines, this version keeps the thresholds in a list of pairs, `(minimum, letter)`, and loops over it from the top. The first pair whose minimum is `<= avg` wins; if none does, the answer is `"F"`. The loop `for minimum, letter in GRADE_TABLE` unpacks each pair, like `for key, value in d.items()` does.

It is the better choice when the scale might change or grow: you edit one line of data instead of the logic. For only five grades, the plain `if` chain in the main solution is just as good and a bit easier for a beginner to read.
