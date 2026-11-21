# Git lifecycle simulation

**What it shows:** how files move from the Working Tree into the Staging Area and then into a committed snapshot.

**Step by step**
1. Lines 1–3 initialize three dictionaries representing `committed`, `staged`, and `working`.
2. Lines 5–7 detect `untracked` files (new in `working`) and `modified` files (changed relative to `staged`).
3. Lines 9–11 simulate `git add` by copying both files into `staged`.
4. Lines 13–14 simulate `git commit` by saving a copy of `staged` as the new `committed` snapshot.

**Try it yourself:** add `"notes.txt": "draft"` to `working` without staging it, then run again and see which list includes it.
