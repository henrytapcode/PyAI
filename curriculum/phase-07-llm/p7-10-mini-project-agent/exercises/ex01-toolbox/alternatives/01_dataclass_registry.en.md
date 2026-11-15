# Single-dictionary registry with dataclass entries

This alternative groups each tool's callable, schema copy, and `side_effect` flag inside a frozen `_ToolEntry` dataclass stored in one insertion-ordered dictionary `_entries`, and extracts argument checking into `_prepare_args()`. Because Python `dict` preserves insertion order, a separate `_order` list is unnecessary, making registration and lookup harder to drift out of sync as the toolbox grows.
