# A logged cleaning run

**What it shows:** a dataset with `None`, a number, an empty text, a link-only text and a duplicate goes through `clean_dataset`. Odd items are warned about, expected drops are only counted, and one `INFO` line sums up the run.

**Step by step**
1. Lines 5–12 set up logging once and create the logger `textclean`. The format shows the level, the logger name and the message.
2. Lines 15–17 are a short `clean_text`: drop link words, join with single spaces, lowercase.
3. Lines 20–25 are the report, a normal (not frozen) dataclass, because the function adds to its counters.
4. Lines 28–45 are `clean_dataset`. A non-string item gets a `WARNING` with its position and is skipped. For a string, an empty result adds to `empty`, a result already in the `seen` set adds to `duplicates`, and anything else is kept.
5. The last lines build the raw list and print the report: two items kept, and the counts `2 2 1` for skipped, empty and duplicates.

**Notice:** the link-only text and the empty text both end up empty, so they count as `empty`. The second reset question is a duplicate of the first once links and capital letters are gone.

**Try it yourself:** change the `level` on line 8 to `logging.WARNING`. The `INFO` summary disappears and the two warnings stay.
