Write `load_and_clean(csv_text)` to turn raw chatbot API log CSV text into a clean pandas `DataFrame`. Write your code inside the function and `return` the cleaned `DataFrame`.

**Example**

Input `csv_text`:

```text
request_id,model,tokens,latency_ms,status,rating
r01, GPT-4o,"1,200",850,ok,5
r01,gpt_4o,999,900,error,1
r02,mini,,N/A,ok,9
```

Returned `DataFrame`:

```text
  request_id   model  tokens  latency_ms status  rating
0        r01  gpt-4o    1200       850.0     ok     5.0
```

**Rules**

- Return columns in exact order: `["request_id", "model", "tokens", "latency_ms", "status", "rating"]`.
- Normalise `model` with `.strip()`, `.lower()`, and replace `"_"` with `"-"`.
- Convert `model` and `tokens` with `.astype(str)` before calling `.str` methods so numeric-only or empty batches do not raise `AttributeError`.
- Parse `tokens` by removing commas `","` and coercing to numbers, then drop duplicate `request_id` rows (keep `"first"`), drop rows where `tokens` is missing, reset the index to `0..n-1`, and cast `tokens` to `"int64"`.
- Coerce `latency_ms` and `rating` to `"float64"` (`NaN` for invalid or missing entries), and turn any `rating` outside `1..5` into `NaN`.
- If every row is invalid (or the CSV has no data rows), return an empty `DataFrame` with all 6 columns in order and `"int64"` dtype for `tokens`.
