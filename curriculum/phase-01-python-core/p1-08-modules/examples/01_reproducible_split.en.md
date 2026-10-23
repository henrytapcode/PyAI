# Reproducible train/test split

**What it shows:** two standard-library modules working together: `random` to shuffle and `statistics` to summarise. This is the same idea as splitting a real dataset into a training set and a test set.

**Step by step**
1. Lines 2–3 import the two modules. `import statistics as st` gives `statistics` a short nickname, so we write `st.mean(...)`.
2. Lines 8–14 define `split_scores`. Line 9 creates a `random.Random(seed)` object: a private random generator that starts from the number you give it. Same seed, same sequence of "random" choices.
3. Line 10 copies the list with `list(values)`, so shuffling does not change `scores`. Line 11 shuffles the copy. Lines 12–13 cut it into a small test part and the rest as train.
4. Lines 17–18 call the function twice with `seed=42`. Line 22 prints `True`: both calls produced exactly the same split.
5. Lines 23–25 use `st.mean` and `st.stdev` (standard deviation, how spread out the numbers are) and round the results.

**Notice:** the numbers look random, but they are not. Run the program ten times and you get the same output ten times. That is what makes an experiment **reproducible**: a teammate can repeat your result.

**Try it yourself:** change `seed=42` to `seed=7` in both calls. The split changes, but the two calls still agree with each other.
