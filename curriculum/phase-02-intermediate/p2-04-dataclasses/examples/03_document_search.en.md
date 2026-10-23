# Document search

**What it shows:** two dataclasses working together. `Document` stores the data. `Hit` has `order=True`, so a list of hits can be sorted without writing any comparison code.

**Step by step**
1. Lines 5–9 define `Document`. Its `tags` list uses `default_factory`, so each document has its own list.
2. Lines 12–15 define `Hit` with `order=True`. Hits compare by `score` first, and by `doc_id` only when the scores are equal.
3. Lines 18–23 create four documents. Only `d1` gets tags.
4. Line 29 counts the word: `text.split()` makes a list of words, and `.count(word)` tells how many times `word` appears in that list.
5. Lines 30–31 keep only documents with a score above 0, as `Hit` objects.
6. Line 32 sorts the hits. `reverse=True` puts the biggest first, so the best match comes first.

**Notice:** `d1` and `d2` both score 1. The tie is broken by `doc_id`, and with `reverse=True` `d2` lands before `d1`.

**Try it yourself:** search for `"pasta"` instead of `"python"`. Only `d3` matches, so only one hit is printed.
