# One text, two configs

**What it shows:** the same `clean_text` function gives different results when you hand it a different `CleanConfig`. The cleaning steps do not change; only the settings do.

**Step by step**
1. Lines 5–9 define the frozen config. Every option has a default, so `CleanConfig()` is the normal setup.
2. Lines 12–18 are the two small pure functions: one fixes spaces, one drops words that start with `http://` or `https://`.
3. Lines 21–33 are `clean_text`. It checks the type, picks the default config when none is given, and runs the steps in a fixed order: links, spaces, case, length.
4. Lines 41–42 make two configs: the normal one, and one that keeps capital letters and cuts to 12 characters.
5. Lines 44–45 print both results for every review, so you can compare them side by side.

**Notice:** in the second column, `Great PRODUC` is cut after 12 characters and `Too SLOW to` has no space at the end, because `rstrip()` removes the space left by the cut.

**Try it yourself:** make a third config, `CleanConfig(drop_urls=False)`, and print the first review with it. The link should stay in the text.
