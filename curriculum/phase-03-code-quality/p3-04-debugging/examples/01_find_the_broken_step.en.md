# Find the broken step

**What it shows:** a three-step text cleaner gives the wrong result for `"GPT-4"`. Printing the value after every step shows which step breaks it.

**Step by step**
1. Lines 5–14 define three small steps: lowercase, remove punctuation, collapse spaces. The regular expression in `remove_punctuation` keeps only letters and spaces.
2. Lines 17–21 define `run`, which applies each step and prints a checkpoint: the step name and the value as `repr`.
3. The first run shows that `lowercase` is fine, but after `remove_punctuation` the `-4` is gone. The bug is in that step, so the other two steps can be ignored.
4. Lines 29–30 redefine `remove_punctuation` so that it also keeps digits and the hyphen. The second run shows `'use gpt-4 now'`.

**Notice:** you did not read the whole program. You compared two neighbouring checkpoints and found the first wrong one.

**Try it yourself:** add a fourth step `strip_stopwords` that removes the word `"now"`, and run again. The new checkpoint should appear at the end, and the first three should not change.
