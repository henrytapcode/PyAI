# Pure classification helper with `collections.Counter`

This alternative extracts per-question grading into a standalone `_classify_case(row, out)` helper and accumulates all summary metrics in a `collections.Counter`. Separating row classification from loop aggregation makes it easy to unit-test individual failure cases in isolation or extend the counter with extra breakdown tags later.
