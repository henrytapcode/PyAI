Implement `score_grounded(answer, expected_facts, context)` in `starter.py`. This is an extended version of `score_answer` from §4: besides fact coverage and unsupported-word checks, a grounded reply must also cite real sources present in `context`.

Write your code inside the function (helper functions are allowed) and `return` a dictionary:

```python
{
    "facts": float,
    "faithful": bool,
    "unsupported": list[str],
    "citations": list[int],
    "bad_citations": list[int],
}
```

## Example cases

Suppose `context` has two source lines:

```text
[1] Refunds are issued within 30 days of purchase.
[2] Standard shipping arrives within 5 business days.
```

| answer | expected_facts | facts | faithful | unsupported | citations | bad_citations |
|---|---|---|---|---|---|---|
| `"Refunds are issued within 30 days. [1]"` | `["30 days"]` | `1.0` | `True` | `[]` | `[1]` | `[]` |
| `"Refunds are issued within 30 days."` | `["30 days"]` | `1.0` | `False` | `[]` | `[]` | `[]` |
| `"Refunds are issued within 30 days. [3]"` | `["30 days"]` | `1.0` | `False` | `[]` | `[3]` | `[3]` |
| `"Shipping takes 5 days [2], refunds 30 days [1] [2]."` | `["5 days", "30 days"]` | `1.0` | `True` | `[]` | `[2, 1]` | `[]` |
| `"I don't know based on the provided context."` | `[]` | `1.0` | `True` | `[]` | `[]` | `[]` |

## Rules

- **`facts` (`float`):**
  - If `expected_facts` is empty, return `1.0` when `"i don't know"` appears in `answer.lower()`, otherwise `0.0`.
  - Otherwise, return the fraction of items in `expected_facts` where `fact.lower() in answer.lower()`.
- **`citations` (`list[int]`):**
  - Extract every integer `n` from `[n]` tags (`\[(\d+)\]`) in `answer`, preserving order of first appearance with no duplicates (e.g. `"[2] ... [1] ... [2]"` gives `[2, 1]`).
  - Compute `citations` the same way even when `answer` contains `"i don't know"`.
- **`bad_citations` (`list[int]`):**
  - `context` is formatted as `"[n] text"` lines joined by `\n`. Extract the valid integer source numbers that appear at the start of a line (allowing optional leading whitespace).
  - `bad_citations` collects the numbers in `citations` (in order) that do not have a matching `[n]` line in `context`.
- **Content-word tokenization and `unsupported` (`list[str]`):**
  1. Lowercase the text.
  2. Remove bracketed citations matching `\[\d+\]` (such as `[1]` or `[12]`).
  3. Extract alphanumeric words matching `[a-z0-9]+`.
  4. Keep only words with `len(word) >= 4`.
  - For example, `"[1] Refunds take 30 days for all items."` produces `["refunds", "take", "days", "items"]` (`[1]`, `30`, `for`, `all` are dropped).
  - If `"i don't know"` appears in `answer.lower()`, `unsupported` is `[]`.
  - Otherwise, `unsupported` collects every content word from `answer` not in the set of content words from `context`, preserving order of first appearance with no duplicates.
- **`faithful` (`bool`):**
  - `True` if `"i don't know"` appears in `answer.lower()`, **or** if `unsupported` is empty **and** `citations` is non-empty **and** `bad_citations` is empty.
  - Otherwise `False` (for example, missing citations or citing `[3]` when `context` only has `[1]` and `[2]`).
- Do not mutate `expected_facts`.
