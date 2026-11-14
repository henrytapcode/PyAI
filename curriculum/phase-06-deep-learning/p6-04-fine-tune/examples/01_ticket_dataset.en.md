# Building and splitting the ticket dataset

**What it shows:** Generating 80 balanced support tickets, splitting them reproducibly into train/val/test, and measuring the longest sequence with the BERT-Tiny tokenizer.

**Step by step**
1. Lines 10–25 define `make_tickets()`, returning 40 `bug` tickets (label `0`) and 40 `billing` tickets (label `1`), including mixed-keyword and synonym edge cases.
2. Lines 28–36 shuffle indices with a seeded `torch.Generator` (`27`) and slice out 48 train, 16 validation, and 16 test tickets, printing per-class counts for each split.
3. Lines 40–42 load the pinned `AutoTokenizer` offline (`local_files_only=True`) and print the maximum token length across all 80 tickets (`10`).

**Notice:** Checking class counts in every split and the maximum token length before training catches empty classes or unexpectedly long inputs before they hit the model.

**Try it yourself:** Change `manual_seed(27)` to `manual_seed(0)` and see how the class balance across `val` and `test` shifts.
