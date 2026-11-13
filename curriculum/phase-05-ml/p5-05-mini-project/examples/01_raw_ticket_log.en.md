# Inspecting the raw ticket log

**What it shows:** Checking a raw 240-row support ticket DataFrame for shape, duplicate IDs, missing values per column, messy `plan` strings, and class imbalance before cleaning.

**Step by step**
1. Lines 7–23 define `make_ticket_log(n=240, seed=21)` to generate raw tickets with comma-formatted strings in `tokens`, missing cells, duplicate `ticket_id` values, messy `plan` labels, and the post-outcome `escalated_to_oncall` leakage column.
2. Lines 26–33 print the raw shape `(240, 7)`, `4` duplicate `ticket_id` rows, and the missing counts (`tokens: 3`, `error_count: 2`).
3. Lines 35–40 print the six messy `plan` variants (`'free'`, `' Free'`, `'pro'`, `' PRO'`, `'enterprise'`, `'Enterprise '`) and the urgent rate `57/240 (0.237)`.

**Notice:** `raw["plan"].value_counts()` splits 3 real plans into 6 categories because of leading/trailing spaces and inconsistent casing.

**Try it yourself:** Print `raw["tokens"].head(8).tolist()` after line 26 to see both comma-formatted strings like `'1,638'` and `None` entries inside the `tokens` column.
