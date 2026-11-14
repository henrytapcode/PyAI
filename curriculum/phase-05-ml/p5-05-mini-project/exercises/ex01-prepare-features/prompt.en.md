Write `prepare_features(raw)` to clean a raw support ticket `DataFrame` into NumPy `(X, y)` arrays while removing the target leakage column. Write your code inside the function and `return` `(X, y)`.

**Example**

Input `raw`:

```text
  ticket_id  plan tokens  error_count  hours_since_deploy  escalated_to_oncall  urgent
0       t01   PRO  1,200          2.0                 4.5                    1       1
1       t01  free    500          0.0                10.0                    0       0
```

Returned `(X, y)`:
- `X`: `array([[1200., 2., 4.5, 1.]])` (`float64`, shape `(1, 4)`)
- `y`: `array([1])` (`"int64"`, shape `(1,)`)

**Rules**

- Do not modify `raw` in place.
- Normalise `plan` with `.astype(str).str.strip().str.lower()` and map `"free" -> 0.0`, `"pro" -> 1.0`, `"enterprise" -> 2.0` (`plan_code`). Unknown plan names become missing (`NaN`) and are dropped.
- Remove commas `","` from `tokens` (using `.astype(str).str.replace(",", "", regex=False)`) and coerce `tokens`, `error_count`, and `hours_since_deploy` to numeric with `pd.to_numeric(..., errors="coerce")`.
- Drop duplicate `ticket_id` rows keeping the first occurrence (`keep="first"`) **before** dropping rows with missing values (matching lesson §3).
- Drop rows with missing `tokens`, `error_count`, `hours_since_deploy`, `plan_code`, or `urgent`.
- Exclude `escalated_to_oncall` (target leakage) from `X`.
- Return `(X, y)` where `X` is a 2D NumPy `"float64"` array with columns in exact order `["tokens", "error_count", "hours_since_deploy", "plan_code"]` and `y` is a 1D NumPy `"int64"` array of `urgent` labels (`0` or `1`). If all rows are dropped, return shape `(0, 4)` for `X` and `(0,)` for `y`.
