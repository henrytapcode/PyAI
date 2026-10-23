# Clean prompts

**What it shows:** normalising text with `lower()`, `split()` and `join()`, then using `in` to spot duplicates.

**Step by step**
1. Lines 2–4 define `normalize(text)`. `text.lower()` makes everything lower-case, `.split()` cuts it into words and drops all extra spaces, and `" ".join(words)` glues the words back with exactly one space.
2. Lines 7–11 hold three raw prompts. The first two differ only in capital letters and spaces. The third is a different request.
3. Lines 13–20 loop over the prompts. Each one is cleaned first (line 15), then `clean in seen` asks whether we already have that exact text.
4. Line 19 adds new prompts to `seen`; line 22 prints how many unique ones remain.

**Notice:** the comparison only works *after* cleaning. `"SUMMARIZE this text"` and `"   Summarize THIS   text  "` are different strings, but their normalised versions are equal. The same trick lets an AI app cache answers for repeated questions.

**Try it yourself:** add `"summarize   this TEXT"` to `raw_prompts`. Predict the output, then run it.
