# Three-way branch merge

**What it shows:** how Git compares `base`, `main`, and `feature` to merge non-conflicting edits and flag conflicts.

**Step by step**
1. Lines 1–3 define three snapshots: common ancestor `base`, `main`, and `feature`.
2. Lines 8–11 iterate over every file name across all three snapshots in sorted order.
3. Lines 13–21 pick the changed side when only one branch modified a file (`app.py` takes `"v2"` from `feature`).
4. Lines 22–25 record a conflict when both branches changed `config.py` differently, keeping `main`'s value in `merged`.

**Try it yourself:** change `feature["config.py"]` to `"port=9000"` (matching `main`) and run again to see `Conflicts` become `[]`.
