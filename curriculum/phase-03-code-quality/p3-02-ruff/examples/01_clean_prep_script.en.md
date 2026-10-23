# A clean price-loading script

**What it shows:** a small data-prep script as it looks *after* a ruff clean-up: every name is used, `None` is checked with `is`, the default list is `None`, and `except` names the error it expects.

**Step by step**
1. Lines 2–8 hold the raw lines, some of them bad (`n/a`, a missing name).
2. Lines 11–15 turn text into a price. `except ValueError` catches only "not a number", so a real bug (like passing `None`) would still show up.
3. Lines 18–24 split one line into a name and a price, and return `None` when either part is unusable.
4. Lines 27–37 loop over the lines. The `skipped` list defaults to `None` and is created inside the function (§6), so two calls never share it.
5. Lines 40–44 call the loader and print the good rows and the skipped lines.

**Notice:** before the clean-up this script had an `import os` nobody used (`F401`), `if row == None` (`E711`), `except:` (`E722`) and `skipped=[]` (`B006`). The output is the same before and after. Clean-up changes how safe the code is, not what it prints on good data.

**Try it yourself:** add the line `"Keyboard,45"` to `RAW_LINES`. The output should list one more good row.
