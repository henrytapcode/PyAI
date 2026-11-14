Your support team wants to flag urgent tickets automatically so they reach the on-call engineer right away. You will go from a messy raw ticket log to a final number your team can actually **trust**. Almost nothing here is new—you are combining everything you learned in phases 4 and 5, and the most important skill is reporting results honestly.

**New in this lesson**
- `make_scorer(f1_score, zero_division=0)` — wraps `f1_score` for `cross_val_score` to make zero-denominator handling explicit (for instance, returning `0.0` if a fold has no predicted positives) instead of relying on the default.
- `cross_val_predict(..., method="predict_proba")` — computes out-of-fold probabilities on the training set so you can choose a decision threshold without touching the test split.
- **Target leakage** — a feature column that only exists *after* the true answer is known, inflating training and CV scores artificially.

## 1. The plan

Map the full workflow from raw logs to an honest report before writing any code:

```mermaid
flowchart LR
    A["Raw log"] --> B["Clean"]
    B --> C["X, y"]
    C --> D["Train / test split"]
    D --> E["5-fold CV on train"]
    E --> F["One test check"]
    F --> G["Honest report"]
```

Split the work into three focused functions, each with one clear job:

| Piece | Input | Output |
|---|---|---|
| `prepare_features(raw)` | raw `DataFrame` | `(X, y)` NumPy arrays (`float64`, `"int64"`) |
| `evaluate_models(X, y, seed)` | training `(X, y)` and `seed` | `{name: (mean, std)}` CV F1 dict |
| `write_report(results, n_test)` | CV dict and `n_test` | list of formatted report lines |

Exercise 1 builds `prepare_features`. Exercise 2 builds `evaluate_models` and `write_report`.

## 2. Inspecting the raw ticket log

Never clean or train blind—generate the raw 240-row ticket log and inspect its shape, duplicate IDs, missing values, messy categories, and urgent class rate first:

```python
import numpy as np
import pandas as pd


def make_ticket_log(n=240, seed=21):
    rng = np.random.default_rng(seed)
    p0 = rng.choice(["free", "pro", "enterprise"], n, p=[0.45, 0.35, 0.20])
    tok, err = rng.integers(150, 2200, n).astype("float64"), rng.poisson(1.3, n).astype("float64")
    hrs = rng.uniform(0.5, 48.0, n).round(1)
    logit = -4.8 + 1.6 * err + 0.002 * tok - 0.08 * hrs + 1.2 * (p0 == "enterprise")
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype("int64")
    m = {"free": " Free", "pro": " PRO", "enterprise": "Enterprise "}
    plans = [m[str(p)] if i % 3 == 0 else str(p) for i, p in enumerate(p0)]
    tok_s = [f"{int(x):,}" if i % 6 == 0 else str(int(x)) for i, x in enumerate(tok)]
    tok_s[5], tok_s[37], tok_s[92], err[[12, 64]] = None, None, None, np.nan
    ids = [f"t{i:03d}" for i in range(n)]
    ids[20], ids[85], ids[140], ids[190] = ids[3], ids[11], ids[25], ids[44]
    leak = np.where(rng.random(n) < 0.98, y, 1 - y).astype("int64")
    return pd.DataFrame({
        "ticket_id": ids, "plan": plans, "tokens": tok_s, "error_count": err,
        "hours_since_deploy": hrs, "escalated_to_oncall": leak, "urgent": y,
    })


raw = make_ticket_log()
print("shape:", raw.shape)
# shape: (240, 7)
print("duplicates:", int(raw["ticket_id"].duplicated().sum()))
# duplicates: 4
print(raw.isna().sum())
# ticket_id              0
# plan                   0
# tokens                 3
# error_count            2
# hours_since_deploy     0
# escalated_to_oncall    0
# urgent                 0
# dtype: int64
print(raw["plan"].value_counts())
# plan
# free           86
# pro            49
#  PRO           31
#  Free          31
# enterprise     25
# Enterprise     18
# Name: count, dtype: int64
print(raw["urgent"].value_counts())
# urgent
# 0    183
# 1     57
# Name: count, dtype: int64
print("urgent rate:", round(float(raw["urgent"].mean()), 3))
# urgent rate: 0.237
```

`make_ticket_log` only **simulates** a raw log so the lesson can run in your browser—you do not need to understand every line inside it; later code blocks copy it verbatim so each block runs on its own.

Look closely at five sample rows to spot every trap in the raw table:

```text
ticket_id  plan         tokens  error_count  escalated_to_oncall  urgent
t003        Free         575           1.0                    0       0   <- leading space + caps
t005       enterprise   None           2.0                    0       0   <- missing tokens
t012       Enterprise    657           NaN                    0       0   <- trailing space + NaN
t003       free         1902           1.0                    0       0   <- duplicate ticket_id
t042       Enterprise  1,638           1.0                    1       1   <- comma + leakage col
```

Only `23.7%` of tickets (`57` out of `240`) are urgent, so plain accuracy will flatter a useless model—and `escalated_to_oncall` records whether an engineer later escalated the ticket, which is unavailable when a new ticket first arrives.

## 3. Part 1: cleaning and building features

Watch how a 5-row slice shrinks and turns numeric step by step: normalise `plan`, strip `","` from `tokens` before calling `pd.to_numeric(..., errors="coerce")`, drop duplicate `ticket_id` rows (`keep="first"`), drop rows with missing numeric values, and map `"free" / "pro" / "enterprise"` to `0.0 / 1.0 / 2.0`. Press **Visualize** on this block and watch `mini` shrink from `5` rows down to `2`:

```python
import numpy as np
import pandas as pd

mini = pd.DataFrame({
    "ticket_id": ["t003", "t005", "t012", "t003", "t042"],
    "plan": [" Free", "enterprise", "Enterprise ", "free", "Enterprise "],
    "tokens": ["575", None, "657", "1902", "1,638"],
    "error_count": [1.0, 2.0, np.nan, 1.0, 1.0],
    "hours_since_deploy": [44.2, 5.0, 36.4, 44.0, 15.0],
    "escalated_to_oncall": [0, 0, 0, 0, 1],
    "urgent": [0, 0, 0, 0, 1],
})
mini["plan"] = mini["plan"].astype(str).str.strip().str.lower()
mini["tokens"] = pd.to_numeric(mini["tokens"].astype(str).str.replace(",", "", regex=False), errors="coerce")
mini = mini.drop_duplicates(subset=["ticket_id"], keep="first")
mini = mini.dropna(subset=["tokens", "error_count", "hours_since_deploy"]).reset_index(drop=True)
mini["plan_code"] = mini["plan"].map({"free": 0.0, "pro": 1.0, "enterprise": 2.0})
print(mini[["ticket_id", "plan_code", "tokens", "error_count"]])
#   ticket_id  plan_code  tokens  error_count
# 0      t003        0.0   575.0          1.0
# 1      t042        2.0  1638.0          1.0
```

Here we **drop** rows with missing numbers rather than filling them with column averages: only 5 of 236 deduplicated rows (`2.1%`) have missing numbers, and dropping them before `train_test_split` avoids inventing values or leaking global means across splits. Now build the full feature matrix `X` (`float64`, fixed column order `["tokens", "error_count", "hours_since_deploy", "plan_code"]`) and label vector `y` (`"int64"`), explicitly leaving out `escalated_to_oncall`:

```python
import numpy as np
import pandas as pd


def make_ticket_log(n=240, seed=21):
    rng = np.random.default_rng(seed)
    p0 = rng.choice(["free", "pro", "enterprise"], n, p=[0.45, 0.35, 0.20])
    tok, err = rng.integers(150, 2200, n).astype("float64"), rng.poisson(1.3, n).astype("float64")
    hrs = rng.uniform(0.5, 48.0, n).round(1)
    logit = -4.8 + 1.6 * err + 0.002 * tok - 0.08 * hrs + 1.2 * (p0 == "enterprise")
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype("int64")
    m = {"free": " Free", "pro": " PRO", "enterprise": "Enterprise "}
    plans = [m[str(p)] if i % 3 == 0 else str(p) for i, p in enumerate(p0)]
    tok_s = [f"{int(x):,}" if i % 6 == 0 else str(int(x)) for i, x in enumerate(tok)]
    tok_s[5], tok_s[37], tok_s[92], err[[12, 64]] = None, None, None, np.nan
    ids = [f"t{i:03d}" for i in range(n)]
    ids[20], ids[85], ids[140], ids[190] = ids[3], ids[11], ids[25], ids[44]
    leak = np.where(rng.random(n) < 0.98, y, 1 - y).astype("int64")
    return pd.DataFrame({
        "ticket_id": ids, "plan": plans, "tokens": tok_s, "error_count": err,
        "hours_since_deploy": hrs, "escalated_to_oncall": leak, "urgent": y,
    })


df = make_ticket_log()
df["plan"] = df["plan"].astype(str).str.strip().str.lower()
df["tokens"] = pd.to_numeric(df["tokens"].astype(str).str.replace(",", "", regex=False), errors="coerce")
df["error_count"] = pd.to_numeric(df["error_count"], errors="coerce")
df["hours_since_deploy"] = pd.to_numeric(df["hours_since_deploy"], errors="coerce")
df = df.drop_duplicates(subset=["ticket_id"], keep="first")
df["plan_code"] = df["plan"].map({"free": 0.0, "pro": 1.0, "enterprise": 2.0})
df = df.dropna(subset=["tokens", "error_count", "hours_since_deploy", "plan_code"]).reset_index(drop=True)

X = df[["tokens", "error_count", "hours_since_deploy", "plan_code"]].to_numpy(dtype="float64")
y = df["urgent"].to_numpy(dtype="int64")
print("X shape:", X.shape, "y urgent:", int(y.sum()), "of", len(y))
# X shape: (231, 4) y urgent: 57 of 231
```

| problem | fix |
|---|---|
| Spaces and mixed case in `plan` | `.astype(str).str.strip().str.lower()`, then map to `0.0 / 1.0 / 2.0` |
| Commas in `tokens` (`"1,638"`) | `.astype(str).str.replace(",", "", regex=False)` then `pd.to_numeric(..., errors="coerce")` |
| Duplicate `ticket_id` rows | `df.drop_duplicates(subset=["ticket_id"], keep="first")` |
| Missing numeric cells (`NaN`) | `df.dropna(subset=["tokens", "error_count", "hours_since_deploy", "plan_code"])` |
| Post-outcome `escalated_to_oncall` | Exclude from the feature column list passed into `X` |

## 4. Part 2: baseline and model selection with CV

Split `25%` of the clean rows into a holdout `test` set with `stratify=y` and lock it away. Run 5-fold `StratifiedKFold(n_splits=5, shuffle=True, random_state=0)` strictly on `(X_train, y_train)`, passing `make_scorer(f1_score, zero_division=0)` to state explicitly that F1 returns `0.000` whenever a fold has a zero denominator (rather than relying on defaults):

```python
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


def make_ticket_log(n=240, seed=21):
    rng = np.random.default_rng(seed)
    p0 = rng.choice(["free", "pro", "enterprise"], n, p=[0.45, 0.35, 0.20])
    tok, err = rng.integers(150, 2200, n).astype("float64"), rng.poisson(1.3, n).astype("float64")
    hrs = rng.uniform(0.5, 48.0, n).round(1)
    logit = -4.8 + 1.6 * err + 0.002 * tok - 0.08 * hrs + 1.2 * (p0 == "enterprise")
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype("int64")
    m = {"free": " Free", "pro": " PRO", "enterprise": "Enterprise "}
    plans = [m[str(p)] if i % 3 == 0 else str(p) for i, p in enumerate(p0)]
    tok_s = [f"{int(x):,}" if i % 6 == 0 else str(int(x)) for i, x in enumerate(tok)]
    tok_s[5], tok_s[37], tok_s[92], err[[12, 64]] = None, None, None, np.nan
    ids = [f"t{i:03d}" for i in range(n)]
    ids[20], ids[85], ids[140], ids[190] = ids[3], ids[11], ids[25], ids[44]
    leak = np.where(rng.random(n) < 0.98, y, 1 - y).astype("int64")
    return pd.DataFrame({
        "ticket_id": ids, "plan": plans, "tokens": tok_s, "error_count": err,
        "hours_since_deploy": hrs, "escalated_to_oncall": leak, "urgent": y,
    })


df = make_ticket_log()
df["plan"] = df["plan"].astype(str).str.strip().str.lower()
df["tokens"] = pd.to_numeric(df["tokens"].astype(str).str.replace(",", "", regex=False), errors="coerce")
df["error_count"] = pd.to_numeric(df["error_count"], errors="coerce")
df["hours_since_deploy"] = pd.to_numeric(df["hours_since_deploy"], errors="coerce")
df = df.drop_duplicates(subset=["ticket_id"], keep="first")
df["plan_code"] = df["plan"].map({"free": 0.0, "pro": 1.0, "enterprise": 2.0})
df = df.dropna(subset=["tokens", "error_count", "hours_since_deploy", "plan_code"]).reset_index(drop=True)

X = df[["tokens", "error_count", "hours_since_deploy", "plan_code"]].to_numpy(dtype="float64")
y = df["urgent"].to_numpy(dtype="int64")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
f1_safe = make_scorer(f1_score, zero_division=0)
models = [
    ("baseline", DummyClassifier(strategy="most_frequent")),
    ("logreg", make_pipeline(StandardScaler(), LogisticRegression())),
    ("tree", DecisionTreeClassifier(max_depth=3, random_state=0)),
]

for name, est in models:
    scores = cross_val_score(est, X_train, y_train, cv=skf, scoring=f1_safe)
    print(f"{name:<8} mean={round(float(scores.mean()), 3):.3f} std={round(float(scores.std()), 3):.3f}")
# baseline mean=0.000 std=0.000
# logreg   mean=0.709 std=0.092
# tree     mean=0.701 std=0.140
```

| model | CV F1 mean | CV F1 std |
|---|---|---|
| `baseline` (`DummyClassifier`) | `0.000` | `0.000` |
| `logreg` (`StandardScaler` + `LogisticRegression`) | `0.709` | `0.092` |
| `tree` (`DecisionTreeClassifier(max_depth=3)`) | `0.701` | `0.140` |

Both real models beat `baseline` (`0.000`) clearly, and `logreg` edges out `tree` (`0.709` vs `0.701`) with a tighter fold-to-fold spread (`0.092` vs `0.140`). Notice the gap (`0.008`) is much smaller than either standard deviation—we will flag that honestly in the final report.

## 5. Part 3: one final evaluation on the test set

For urgent tickets, missing a real incident hurts more than checking a false alarm, so we want `recall >= 0.80`—and we must choose that threshold **using only training CV**, never by peeking at `X_test`. Calling `cross_val_predict(pipe, X_train, y_train, cv=skf, method="predict_proba")` gives out-of-fold probabilities where each training ticket is scored by a model that never trained on it:

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def make_ticket_log(n=240, seed=21):
    rng = np.random.default_rng(seed)
    p0 = rng.choice(["free", "pro", "enterprise"], n, p=[0.45, 0.35, 0.20])
    tok, err = rng.integers(150, 2200, n).astype("float64"), rng.poisson(1.3, n).astype("float64")
    hrs = rng.uniform(0.5, 48.0, n).round(1)
    logit = -4.8 + 1.6 * err + 0.002 * tok - 0.08 * hrs + 1.2 * (p0 == "enterprise")
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype("int64")
    m = {"free": " Free", "pro": " PRO", "enterprise": "Enterprise "}
    plans = [m[str(p)] if i % 3 == 0 else str(p) for i, p in enumerate(p0)]
    tok_s = [f"{int(x):,}" if i % 6 == 0 else str(int(x)) for i, x in enumerate(tok)]
    tok_s[5], tok_s[37], tok_s[92], err[[12, 64]] = None, None, None, np.nan
    ids = [f"t{i:03d}" for i in range(n)]
    ids[20], ids[85], ids[140], ids[190] = ids[3], ids[11], ids[25], ids[44]
    leak = np.where(rng.random(n) < 0.98, y, 1 - y).astype("int64")
    return pd.DataFrame({
        "ticket_id": ids, "plan": plans, "tokens": tok_s, "error_count": err,
        "hours_since_deploy": hrs, "escalated_to_oncall": leak, "urgent": y,
    })


df = make_ticket_log()
df["plan"] = df["plan"].astype(str).str.strip().str.lower()
df["tokens"] = pd.to_numeric(df["tokens"].astype(str).str.replace(",", "", regex=False), errors="coerce")
df["error_count"] = pd.to_numeric(df["error_count"], errors="coerce")
df["hours_since_deploy"] = pd.to_numeric(df["hours_since_deploy"], errors="coerce")
df = df.drop_duplicates(subset=["ticket_id"], keep="first")
df["plan_code"] = df["plan"].map({"free": 0.0, "pro": 1.0, "enterprise": 2.0})
df = df.dropna(subset=["tokens", "error_count", "hours_since_deploy", "plan_code"]).reset_index(drop=True)

X = df[["tokens", "error_count", "hours_since_deploy", "plan_code"]].to_numpy(dtype="float64")
y = df["urgent"].to_numpy(dtype="int64")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
pipe = make_pipeline(StandardScaler(), LogisticRegression())
oof_probs = cross_val_predict(pipe, X_train, y_train, cv=skf, method="predict_proba")[:, 1]

for t in [0.5, 0.4, 0.3, 0.2]:
    oof_preds = (oof_probs >= t).astype("int64")
    p = round(float(precision_score(y_train, oof_preds, zero_division=0)), 3)
    r = round(float(recall_score(y_train, oof_preds)), 3)
    f = round(float(f1_score(y_train, oof_preds, zero_division=0)), 3)
    print(f"t={t} prec={p:.3f} rec={r:.3f} f1={f:.3f}")
# t=0.5 prec=0.818 rec=0.628 f1=0.711
# t=0.4 prec=0.732 rec=0.698 f1=0.714
# t=0.3 prec=0.627 rec=0.744 f1=0.681
# t=0.2 prec=0.507 rec=0.837 f1=0.632

pipe.fit(X_train, y_train)
test_preds = (pipe.predict_proba(X_test)[:, 1] >= 0.2).astype("int64")
print("cm:", confusion_matrix(y_test, test_preds).tolist())
# cm: [[31, 13], [1, 13]]
print(
    "test prec:", round(float(precision_score(y_test, test_preds, zero_division=0)), 3),
    "rec:", round(float(recall_score(y_test, test_preds)), 3),
    "f1:", round(float(f1_score(y_test, test_preds, zero_division=0)), 3),
)
# test prec: 0.5 rec: 0.929 f1: 0.65
```

Trace the training out-of-fold threshold sweep:

| threshold | OOF precision | OOF recall | OOF F1 | meets `recall >= 0.80`? |
|---|---|---|---|---|
| `0.5` | `0.818` | `0.628` | `0.711` | no |
| `0.4` | `0.732` | `0.698` | `0.714` | no |
| `0.3` | `0.627` | `0.744` | `0.681` | no |
| `0.2` | `0.507` | `0.837` | `0.632` | yes (`0.2` chosen) |

Locked to threshold `0.2` before touching `X_test`, the final fit catches `13` of `14` urgent test tickets (`recall = 0.929`, `FN = 1`) at the cost of `13` false alarms (`FP = 13`, `precision = 0.5`).

## 6. Part 4: writing an honest report

Put every piece together into a short, transparent summary that states the sample size, the baseline, the CV uncertainty (`mean +/- std`), the single test check, and the statistical tie between `logreg` and `tree`:

```python
n_test = 58
n_urgent = 14
base_acc, base_f1 = 0.759, 0.0
lr_mean, lr_std = 0.709, 0.092
tr_mean, tr_std = 0.701, 0.140
test_prec, test_rec, test_f1 = 0.5, 0.929, 0.65

print(f"test set: {n_test} tickets ({n_urgent} urgent)")
# test set: 58 tickets (14 urgent)
print(f"baseline: acc={base_acc:.3f} F1={base_f1:.3f}")
# baseline: acc=0.759 F1=0.000
print(f"logreg CV F1: {lr_mean:.3f} +/- {lr_std:.3f}")
# logreg CV F1: 0.709 +/- 0.092
print(f"tree   CV F1: {tr_mean:.3f} +/- {tr_std:.3f}")
# tree   CV F1: 0.701 +/- 0.140
print(f"test @ t=0.2: prec={test_prec:.3f} rec={test_rec:.3f} F1={test_f1:.3f}")
# test @ t=0.2: prec=0.500 rec=0.929 F1=0.650
if abs(lr_mean - tr_mean) < max(lr_std, tr_std):
    print("note: logreg and tree differ by less than one std; cannot claim one is clearly better")
# note: logreg and tree differ by less than one std; cannot claim one is clearly better
```

| honest claim | misleading claim |
|---|---|
| "CV F1 `0.709 +/- 0.092` across 5 folds vs `0.000` baseline" | "Our classifier achieves 76% accuracy!" |
| "Tested once on `58` held-out tickets (`14` urgent); recall `0.929`, precision `0.500`" | "Our model catches 93% of urgent tickets" (hiding sample size and false alarms) |
| "`logreg` (`0.709`) and `tree` (`0.701`) differ by less than one std (`0.008 < 0.140`)" | "`logreg` is proven superior to decision trees" |

> [!TIP]
> Always report your **baseline** and **test sample size** (`n_test` and the minority class count). Without the baseline, `0.759` accuracy sounds useful when it catches zero urgent tickets; without `n_test = 58 (14 urgent)`, a reader cannot judge how noisy one misclassified ticket is.

## 7. Common mistakes

**1. Target leakage (`escalated_to_oncall`)**

Keeping a column recorded *after* the ticket is handled gives the model the answer in disguise—when a brand-new ticket arrives, `escalated_to_oncall` does not exist yet. Fix: drop post-outcome columns before building `X`.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, make_scorer
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def make_ticket_log(n=240, seed=21):
    rng = np.random.default_rng(seed)
    p0 = rng.choice(["free", "pro", "enterprise"], n, p=[0.45, 0.35, 0.20])
    tok, err = rng.integers(150, 2200, n).astype("float64"), rng.poisson(1.3, n).astype("float64")
    hrs = rng.uniform(0.5, 48.0, n).round(1)
    logit = -4.8 + 1.6 * err + 0.002 * tok - 0.08 * hrs + 1.2 * (p0 == "enterprise")
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype("int64")
    m = {"free": " Free", "pro": " PRO", "enterprise": "Enterprise "}
    plans = [m[str(p)] if i % 3 == 0 else str(p) for i, p in enumerate(p0)]
    tok_s = [f"{int(x):,}" if i % 6 == 0 else str(int(x)) for i, x in enumerate(tok)]
    tok_s[5], tok_s[37], tok_s[92], err[[12, 64]] = None, None, None, np.nan
    ids = [f"t{i:03d}" for i in range(n)]
    ids[20], ids[85], ids[140], ids[190] = ids[3], ids[11], ids[25], ids[44]
    leak = np.where(rng.random(n) < 0.98, y, 1 - y).astype("int64")
    return pd.DataFrame({
        "ticket_id": ids, "plan": plans, "tokens": tok_s, "error_count": err,
        "hours_since_deploy": hrs, "escalated_to_oncall": leak, "urgent": y,
    })


df = make_ticket_log()
df["plan"] = df["plan"].astype(str).str.strip().str.lower()
df["tokens"] = pd.to_numeric(df["tokens"].astype(str).str.replace(",", "", regex=False), errors="coerce")
df = df.drop_duplicates(subset=["ticket_id"], keep="first")
df["plan_code"] = df["plan"].map({"free": 0.0, "pro": 1.0, "enterprise": 2.0})
df = df.dropna(subset=["tokens", "error_count", "hours_since_deploy", "plan_code"]).reset_index(drop=True)

y = df["urgent"].to_numpy(dtype="int64")
X_clean = df[["tokens", "error_count", "hours_since_deploy", "plan_code"]].to_numpy(dtype="float64")
X_leak = df[["tokens", "error_count", "hours_since_deploy", "plan_code", "escalated_to_oncall"]].to_numpy(dtype="float64")

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
f1_safe = make_scorer(f1_score, zero_division=0)
pipe = make_pipeline(StandardScaler(), LogisticRegression())

X_tr_l, _, y_tr_l, _ = train_test_split(X_leak, y, test_size=0.25, stratify=y, random_state=42)
X_tr_c, _, y_tr_c, _ = train_test_split(X_clean, y, test_size=0.25, stratify=y, random_state=42)

# Wrong: escalated_to_oncall leaks the post-resolution answer -> suspiciously near 1.0
s_leak = cross_val_score(pipe, X_tr_l, y_tr_l, cv=skf, scoring=f1_safe)
# Fix: drop escalated_to_oncall before splitting and training
s_clean = cross_val_score(pipe, X_tr_c, y_tr_c, cv=skf, scoring=f1_safe)
print("with leakage:", round(float(s_leak.mean()), 3), "+/-", round(float(s_leak.std()), 3))
# with leakage: 0.978 +/- 0.027
print("clean       :", round(float(s_clean.mean()), 3), "+/-", round(float(s_clean.std()), 3))
# clean       : 0.709 +/- 0.092
```

**2. Tuning the decision threshold on the test set**

Sweeping thresholds directly on `X_test` to pick the highest test F1 fits your cutoff to the `58` test rows and leaves no unseen data to verify it. Fix: pick the threshold on `X_train` with `cross_val_predict`, then evaluate `X_test` once.

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def make_ticket_log(n=240, seed=21):
    rng = np.random.default_rng(seed)
    p0 = rng.choice(["free", "pro", "enterprise"], n, p=[0.45, 0.35, 0.20])
    tok, err = rng.integers(150, 2200, n).astype("float64"), rng.poisson(1.3, n).astype("float64")
    hrs = rng.uniform(0.5, 48.0, n).round(1)
    logit = -4.8 + 1.6 * err + 0.002 * tok - 0.08 * hrs + 1.2 * (p0 == "enterprise")
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype("int64")
    m = {"free": " Free", "pro": " PRO", "enterprise": "Enterprise "}
    plans = [m[str(p)] if i % 3 == 0 else str(p) for i, p in enumerate(p0)]
    tok_s = [f"{int(x):,}" if i % 6 == 0 else str(int(x)) for i, x in enumerate(tok)]
    tok_s[5], tok_s[37], tok_s[92], err[[12, 64]] = None, None, None, np.nan
    ids = [f"t{i:03d}" for i in range(n)]
    ids[20], ids[85], ids[140], ids[190] = ids[3], ids[11], ids[25], ids[44]
    leak = np.where(rng.random(n) < 0.98, y, 1 - y).astype("int64")
    return pd.DataFrame({
        "ticket_id": ids, "plan": plans, "tokens": tok_s, "error_count": err,
        "hours_since_deploy": hrs, "escalated_to_oncall": leak, "urgent": y,
    })


df = make_ticket_log()
df["plan"] = df["plan"].astype(str).str.strip().str.lower()
df["tokens"] = pd.to_numeric(df["tokens"].astype(str).str.replace(",", "", regex=False), errors="coerce")
df = df.drop_duplicates(subset=["ticket_id"], keep="first")
df["plan_code"] = df["plan"].map({"free": 0.0, "pro": 1.0, "enterprise": 2.0})
df = df.dropna(subset=["tokens", "error_count", "hours_since_deploy", "plan_code"]).reset_index(drop=True)

X = df[["tokens", "error_count", "hours_since_deploy", "plan_code"]].to_numpy(dtype="float64")
y = df["urgent"].to_numpy(dtype="int64")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)
test_probs = pipe.predict_proba(X_test)[:, 1]
# Wrong: picking the threshold that peaks on X_test leaves no unseen split left
best_on_test = max(
    [0.5, 0.4, 0.3, 0.25, 0.2],
    key=lambda t: float(f1_score(y_test, (test_probs >= t).astype("int64"), zero_division=0)),
)
print("peeked test t:", best_on_test, "F1:", round(float(f1_score(y_test, (test_probs >= best_on_test).astype("int64"))), 3))
# peeked test t: 0.25 F1: 0.667

# Fix: pick threshold on train OOF probabilities for recall >= 0.80, then score test once
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
oof = cross_val_predict(pipe, X_train, y_train, cv=skf, method="predict_proba")[:, 1]
honest_t = next(t for t in [0.5, 0.4, 0.3, 0.2] if float(recall_score(y_train, (oof >= t).astype("int64"))) >= 0.80)
print("honest train t:", honest_t, "test F1:", round(float(f1_score(y_test, (test_probs >= honest_t).astype("int64"))), 3))
# honest train t: 0.2 test F1: 0.65
```

**3. Reporting accuracy instead of F1/recall on imbalanced data**

On these `58` test tickets (`14` urgent), `DummyClassifier` and our tuned `logreg` score the exact same accuracy (`0.759`), yet one catches `0` urgent tickets while the other catches `13` of `14`:

```python
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def make_ticket_log(n=240, seed=21):
    rng = np.random.default_rng(seed)
    p0 = rng.choice(["free", "pro", "enterprise"], n, p=[0.45, 0.35, 0.20])
    tok, err = rng.integers(150, 2200, n).astype("float64"), rng.poisson(1.3, n).astype("float64")
    hrs = rng.uniform(0.5, 48.0, n).round(1)
    logit = -4.8 + 1.6 * err + 0.002 * tok - 0.08 * hrs + 1.2 * (p0 == "enterprise")
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype("int64")
    m = {"free": " Free", "pro": " PRO", "enterprise": "Enterprise "}
    plans = [m[str(p)] if i % 3 == 0 else str(p) for i, p in enumerate(p0)]
    tok_s = [f"{int(x):,}" if i % 6 == 0 else str(int(x)) for i, x in enumerate(tok)]
    tok_s[5], tok_s[37], tok_s[92], err[[12, 64]] = None, None, None, np.nan
    ids = [f"t{i:03d}" for i in range(n)]
    ids[20], ids[85], ids[140], ids[190] = ids[3], ids[11], ids[25], ids[44]
    leak = np.where(rng.random(n) < 0.98, y, 1 - y).astype("int64")
    return pd.DataFrame({
        "ticket_id": ids, "plan": plans, "tokens": tok_s, "error_count": err,
        "hours_since_deploy": hrs, "escalated_to_oncall": leak, "urgent": y,
    })


df = make_ticket_log()
df["plan"] = df["plan"].astype(str).str.strip().str.lower()
df["tokens"] = pd.to_numeric(df["tokens"].astype(str).str.replace(",", "", regex=False), errors="coerce")
df = df.drop_duplicates(subset=["ticket_id"], keep="first")
df["plan_code"] = df["plan"].map({"free": 0.0, "pro": 1.0, "enterprise": 2.0})
df = df.dropna(subset=["tokens", "error_count", "hours_since_deploy", "plan_code"]).reset_index(drop=True)

X = df[["tokens", "error_count", "hours_since_deploy", "plan_code"]].to_numpy(dtype="float64")
y = df["urgent"].to_numpy(dtype="int64")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

base = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)
b_preds = base.predict(X_test)
m_preds = (pipe.predict_proba(X_test)[:, 1] >= 0.2).astype("int64")

print("baseline acc:", round(float(accuracy_score(y_test, b_preds)), 3), "f1:", round(float(f1_score(y_test, b_preds, zero_division=0)), 3))
# baseline acc: 0.759 f1: 0.0
print("logreg   acc:", round(float(accuracy_score(y_test, m_preds)), 3), "f1:", round(float(f1_score(y_test, m_preds, zero_division=0)), 3))
# logreg   acc: 0.759 f1: 0.65
```

## Recap

- Inspect raw logs first (`shape`, `isna().sum()`, `value_counts()`, duplicate IDs) and drop post-outcome **target leakage** columns before building `X`.
- Clean categories, numbers, duplicates (`keep="first"`), and missing rows into a fixed-order `float64` matrix `X` and `"int64"` array `y`.
- Lock away a stratified holdout `test` split from the start; run 5-fold `StratifiedKFold` CV against a `DummyClassifier` baseline using `make_scorer(f1_score, zero_division=0)`.
- Tune decision thresholds strictly on training CV (`cross_val_predict`), then score `test` **once**.
- Report `baseline`, sample size (`n_test` and positive count), `mean +/- std`, and warn whenever candidate models differ by less than one standard deviation.

## Take it further

Once both exercises pass, try extending your classifier workflow:

- Add a ratio feature such as `tokens / (error_count + 1)` and check whether 5-fold CV F1 improves on `X_train`.
- Pass `class_weight="balanced"` to `LogisticRegression` and compare precision and recall at the default `0.5` threshold.
- Plot a precision-and-recall curve across thresholds `[0.1, 0.2, 0.3, 0.4, 0.5, 0.6]` using out-of-fold probabilities from `X_train`.
