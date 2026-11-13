# Inspecting raw API logs

**What it shows:** how to scan a raw CSV log table for shape, missing cells, inconsistent model names, and duplicate request IDs before cleaning anything.

**Step by step**
1. Lines 5–19 store the 14-row raw chatbot log inline as CSV text.
2. Line 21 loads the CSV into a DataFrame with `pd.read_csv(io.StringIO(csv_text))`.
3. Lines 22–26 print the table shape, missing-value count per column, distinct raw model names, and duplicate `request_id` count.

**Notice:** `latency_ms` shows only `1` missing cell right now (`N/A`), even though row `r09` holds `"timeout"`—`pd.read_csv` leaves `"timeout"` as text until we coerce the column to numbers.

**Try it yourself:** print `df.dtypes` right after `pd.read_csv(...)` to see which numeric-looking columns were read as `object`.
