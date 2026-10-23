# Prompt lengths

**What it shows:** the three basic comprehensions on one list of prompts: a list of numbers, a dict, and a filtered list.

**Step by step**
1. Lines 2–7 create a list of four prompts.
2. Line 9 builds a list of word counts. `p.split()` cuts a prompt into words and `len(...)` counts them, so the output is `[3, 1, 5, 3]`.
3. Line 12 uses curly braces and `key: value` to build a dict from each prompt to its word count. Line 13 looks one up.
4. Line 15 adds `if` at the end, so only prompts with at least 3 words are kept.
5. Line 18 uses `max` on the list from line 9 to find the biggest number.

**Notice:** the result of a comprehension is a brand new collection. `prompts` itself never changes.

**Try it yourself:** change `>= 3` on line 15 to `>= 5`. Only one prompt should be left.
