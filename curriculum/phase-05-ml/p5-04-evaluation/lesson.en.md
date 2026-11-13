Suppose 85% of incoming support tickets are normal and only 15% are urgent. A "model" that ignores the text and blindly answers "normal" every time reaches 0.85 accuracy while missing every single urgent ticket. Evaluating a model is about picking the right number for the question your team actually cares about.

## 1. The accuracy trap on imbalanced data

When one class is much rarer than another (**imbalanced data**), plain **accuracy** can look impressive even when the model is useless. Always measure a simple **baseline** first — a trivial rule like predicting the most frequent class — before celebrating a score.

`DummyClassifier` from `sklearn.dummy` builds rule-based baseline classifiers (`strategy="most_frequent"` always predicts the majority training label), so you can see the floor your real model must beat.

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(
    n_samples=200, n_features=5, weights=[0.85], random_state=1
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0, stratify=y
)

baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)

print("test counts:", np.bincount(y_test, minlength=2).tolist())  # test counts: [51, 9]
print("baseline acc:", round(float(baseline.score(X_test, y_test)), 3))  # baseline acc: 0.85
print("model acc:", round(float(pipe.score(X_test, y_test)), 3))        # model acc: 0.883
```

Notice that `LogisticRegression` hits `0.883` accuracy, only `0.033` above the dummy `0.85` baseline — accuracy alone cannot tell us how many of the `9` urgent tickets it actually caught. Always compare against a baseline.

## 2. The confusion matrix

A **confusion matrix** splits predictions into four cells instead of one overall percentage: **True Positive (TP)** and **True Negative (TN)** are correct predictions, while **False Positive (FP)** (false alarm) and **False Negative (FN)** (missed urgent ticket) are the two kinds of mistakes.

In `scikit-learn`, `confusion_matrix(y_true, y_pred)` from `sklearn.metrics` places actual labels on rows and predicted labels on columns:

```text
              predicted 0    predicted 1
actual 0   [     TN       ,     FP       ]
actual 1   [     FN       ,     TP       ]
```

Let's count all four cells manually with NumPy boolean masks (treating `1` = urgent as the positive class) and compare against `confusion_matrix(y_test, preds).tolist()`.

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(
    n_samples=200, n_features=5, weights=[0.85], random_state=1
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0, stratify=y
)
pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)
preds = pipe.predict(X_test)

tn = int(((y_test == 0) & (preds == 0)).sum())
fp = int(((y_test == 0) & (preds == 1)).sum())
fn = int(((y_test == 1) & (preds == 0)).sum())
tp = int(((y_test == 1) & (preds == 1)).sum())

print("manual: ", [[tn, fp], [fn, tp]])                    # manual:  [[51, 0], [7, 2]]
print("sklearn:", confusion_matrix(y_test, preds).tolist())  # sklearn: [[51, 0], [7, 2]]
```

Notice that `51 + 0 + 7 + 2 = 60` test tickets, and out of `9` actual urgent tickets (`FN + TP = 7 + 2`), the model missed `7` and caught only `2`!

| cell | meaning | ticket example |
|---|---|---|
| `TP` | actual positive, predicted positive | urgent ticket routed to the on-call team |
| `FP` | actual negative, predicted positive | normal ticket flagged urgent by mistake |
| `FN` | actual positive, predicted negative | urgent ticket silently dropped into the normal queue |
| `TN` | actual negative, predicted negative | normal ticket kept in the normal queue |

## 3. Precision, recall, and F1

From those four cells we get three focused metrics: **precision** asks *"when the model predicts urgent, how often is it right?"* (`TP / (TP + FP)`), **recall** asks *"out of all truly urgent tickets, how many did it catch?"* (`TP / (TP + FN)`), and the **F1 score** is their harmonic mean (`2 * precision * recall / (precision + recall)`), which drops toward zero if either one is low.

In `sklearn.metrics`, `precision_score(y_true, y_pred)`, `recall_score(y_true, y_pred)`, and `f1_score(y_true, y_pred)` compute these three values directly. When a model makes zero positive predictions (`TP + FP == 0`), dividing by zero triggers an `UndefinedMetricWarning`, so pass `zero_division=0` whenever zero positive predictions are possible.

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(
    n_samples=200, n_features=5, weights=[0.85], random_state=1
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0, stratify=y
)
pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)
preds = pipe.predict(X_test)

tp = int(((y_test == 1) & (preds == 1)).sum())
fp = int(((y_test == 0) & (preds == 1)).sum())
fn = int(((y_test == 1) & (preds == 0)).sum())

prec = tp / (tp + fp)
rec = tp / (tp + fn)
f1 = 2 * prec * rec / (prec + rec)
print("manual: ", round(prec, 3), round(rec, 3), round(f1, 3))
# manual:  1.0 0.222 0.364

print(
    "sklearn:",
    round(float(precision_score(y_test, preds)), 3),
    round(float(recall_score(y_test, preds)), 3),
    round(float(f1_score(y_test, preds)), 3),
)
# sklearn: 1.0 0.222 0.364

all_zero = np.zeros_like(y_test)
print("baseline precision:", round(float(precision_score(y_test, all_zero, zero_division=0)), 3))
# baseline precision: 0.0
```

| metric | formula | value |
|---|---|---|
| precision | `TP / (TP + FP) = 2 / (2 + 0)` | `1.0` |
| recall | `TP / (TP + FN) = 2 / (2 + 7)` | `0.222` |
| F1 score | `2 * 1.0 * 0.222 / (1.0 + 0.222)` | `0.364` |

| situation | care most about | why |
|---|---|---|
| Spam filter | precision | blocking an important real email (`FP`) is worse than letting one spam email through |
| Urgent ticket / fraud detection | recall | missing an outage or fraud case (`FN`) is far costlier than checking a false alarm |
| General imbalanced classifier | F1 score | balances precision and recall in a single number without letting majority class dominate |

## 4. Reading `classification_report`

Instead of calling three separate functions, `classification_report` from `sklearn.metrics` prints a per-class summary table in one call (`digits=3` controls decimal places).

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(
    n_samples=200, n_features=5, weights=[0.85], random_state=1
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0, stratify=y
)
pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)
preds = pipe.predict(X_test)

print(classification_report(y_test, preds, digits=3))
```

```text
              precision    recall  f1-score   support

           0      0.879     1.000     0.936        51
           1      1.000     0.222     0.364         9

    accuracy                          0.883        60
   macro avg      0.940     0.611     0.650        60
weighted avg      0.897     0.883     0.850        60

```

Each column shows `precision`, `recall`, `f1-score`, and `support` (how many true examples of that class exist in `y_test`). `macro avg` takes the unweighted mean across classes (`(0.936 + 0.364) / 2 = 0.650` for F1), treating rare and common classes equally; `weighted avg` weights each class by its `support`, so the `51` normal tickets pull weighted F1 up to `0.850`.

## 5. Decision thresholds and `predict_proba`

Just like the threshold rule you wrote in `p5-02-supervised`, `.predict(X)` does not magically emit `0` or `1` — internally it compares a probability against a **decision threshold** of `0.5`. Calling `.predict_proba(X)[:, 1]` returns the predicted probability of class `1`, letting you lower the threshold to catch more urgent tickets (higher recall) at the cost of more false alarms (lower precision).

Press **Visualize** on this block and watch `preds` and `rec` change as `t` drops from `0.5` down to `0.1`.

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(
    n_samples=200, n_features=5, weights=[0.85], random_state=1
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0, stratify=y
)
pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)
probs = pipe.predict_proba(X_test)[:, 1]

for t in [0.5, 0.3, 0.1]:
    preds = (probs >= t).astype("int64")
    prec = round(float(precision_score(y_test, preds, zero_division=0)), 3)
    rec = round(float(recall_score(y_test, preds)), 3)
    print(f"t={t} prec={prec} rec={rec}")
# t=0.5 prec=1.0 rec=0.222
# t=0.3 prec=0.889 rec=0.889
# t=0.1 prec=0.471 rec=0.889
```

| threshold | precision | recall |
|---|---|---|
| `0.5` | `1.0` | `0.222` |
| `0.3` | `0.889` | `0.889` |
| `0.1` | `0.471` | `0.889` |

Notice how lowering the threshold to `0.3` jumps recall from `0.222` to `0.889` (`8` of `9` urgent tickets caught) while precision stays at `0.889` — whereas dropping further to `0.1` adds false alarms without catching any extra urgent ticket.

## 6. Cross-validation

As noted in `p5-03-sklearn`, a single train/test split still carries luck of the draw depending on which rows land in `test`. **Cross-validation** splits the dataset into `k` equal parts called **folds**, trains on `k - 1` folds and scores on the remaining fold `k` times, then reports the mean and standard deviation (`mean +/- std`) across all folds.

```text
Fold 1: [T][ ][ ][ ][ ]
Fold 2: [ ][T][ ][ ][ ]
Fold 3: [ ][ ][T][ ][ ]
Fold 4: [ ][ ][ ][T][ ]
Fold 5: [ ][ ][ ][ ][T]
```

```mermaid
flowchart LR
    A["Data"] --> B["Split into k folds"]
    B --> C["Train on k-1"]
    C --> D["Score on 1"]
    D --> E["Repeat k times"]
    E --> F["Mean +/- std"]
```

`cross_val_score` from `sklearn.model_selection` runs this loop automatically (`cv=5` uses 5 stratified folds for classifiers), and `StratifiedKFold` from `sklearn.model_selection` lets you fix `shuffle=True, random_state=0` and pass `scoring="f1"` to compare models fairly on imbalanced data.

```python
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(
    n_samples=200, n_features=5, weights=[0.85], random_state=1
)

pipe = make_pipeline(StandardScaler(), LogisticRegression())
acc_scores = cross_val_score(pipe, X, y, cv=5)
print("5-fold acc:", np.round(acc_scores, 3).tolist())
# 5-fold acc: [0.9, 0.9, 0.825, 0.925, 0.925]
print("mean +/- std:", round(float(acc_scores.mean()), 3), "+/-", round(float(acc_scores.std()), 3))
# mean +/- std: 0.895 +/- 0.037

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
lr_f1 = cross_val_score(pipe, X, y, cv=skf, scoring="f1")
tree_f1 = cross_val_score(
    DecisionTreeClassifier(max_depth=3, random_state=0), X, y, cv=skf, scoring="f1"
)
print("LogReg F1:", round(float(lr_f1.mean()), 3), "+/-", round(float(lr_f1.std()), 3))
# LogReg F1: 0.597 +/- 0.098
print("Tree   F1:", round(float(tree_f1.mean()), 3), "+/-", round(float(tree_f1.std()), 3))
# Tree   F1: 0.77 +/- 0.066
```

Notice that on 5-fold F1, `DecisionTreeClassifier(max_depth=3)` beats the linear `LogisticRegression` pipeline (`0.77 +/- 0.066` vs `0.597 +/- 0.098`) with lower spread across folds.

> [!TIP]
> Always put `StandardScaler()` **inside** `make_pipeline(...)` before passing the estimator to `cross_val_score`. That guarantees each fold fits the scaler strictly on its own `k - 1` training folds and transforms the held-out fold without leaking test statistics.

## 7. Common mistakes

**1. Checking only accuracy on an imbalanced dataset**

When 95% of rows belong to class `0`, predicting all zeros achieves `0.95` accuracy while catching `0.0` of the rare class. Always inspect `recall_score` or `f1_score` (passing `zero_division=0`) for the minority class.

```python
import numpy as np
from sklearn.metrics import accuracy_score, recall_score

y_true = np.array([0] * 19 + [1])
y_pred = np.zeros_like(y_true)

print("accuracy:", round(float(accuracy_score(y_true, y_pred)), 3))               # accuracy: 0.95
print("recall:  ", round(float(recall_score(y_true, y_pred, zero_division=0)), 3))  # recall:   0.0
```

**2. Swapping `y_true` and `y_pred` in `confusion_matrix`**

Passing `(y_pred, y_true)` instead of `(y_true, y_pred)` transposes the matrix and swaps `FP` with `FN`. Always pass true labels first and predicted labels second.

```python
import numpy as np
from sklearn.metrics import confusion_matrix

y_true = np.array([0, 0, 0, 1, 1, 1])
y_pred = np.array([0, 0, 1, 0, 0, 1])

# Wrong: swapped arguments transpose FP (1) and FN (2)
print("swapped:", confusion_matrix(y_pred, y_true).tolist())  # swapped: [[2, 2], [1, 1]]
# Fix: y_true first, y_pred second
print("correct:", confusion_matrix(y_true, y_pred).tolist())  # correct: [[2, 1], [2, 1]]
```

**3. Scaling the full `X` before `cross_val_score` (data leakage)**

Fitting `StandardScaler` on all of `X` before cross-validation leaks the mean and standard deviation of every validation fold into training. Even when two small synthetic numbers look identical (`0.895` vs `0.895` below), the leaked workflow is invalid and can inflate scores on skewed real data — put the scaler inside `make_pipeline`.

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(
    n_samples=200, n_features=5, weights=[0.85], random_state=1
)

# Wrong: scaler sees every fold before splitting
X_scaled = StandardScaler().fit_transform(X)
leaked = cross_val_score(LogisticRegression(), X_scaled, y, cv=5)

# Fix: scaler lives inside the pipeline
pipe = make_pipeline(StandardScaler(), LogisticRegression())
clean = cross_val_score(pipe, X, y, cv=5)

print("leaked mean:", round(float(leaked.mean()), 3))  # leaked mean: 0.895
print("clean mean: ", round(float(clean.mean()), 3))   # clean mean:  0.895
```

**4. Reporting mean CV without `std`, or picking by one lucky fold**

Two models can share the exact same single-fold peak (`0.727` below) while having different stability across folds. Report both `mean` and `std`, and choose by `mean` + stability rather than cherry-picking `.max()`.

```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(
    n_samples=200, n_features=5, weights=[0.85], random_state=1
)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

for name, est in [("LogReg", LogisticRegression()), ("KNN(k=1)", KNeighborsClassifier(n_neighbors=1))]:
    scores = cross_val_score(make_pipeline(StandardScaler(), est), X, y, cv=skf, scoring="f1")
    print(
        f"{name:<8} mean={round(float(scores.mean()), 3)}"
        f" std={round(float(scores.std()), 3)} best={round(float(scores.max()), 3)}"
    )
# LogReg   mean=0.597 std=0.098 best=0.727
# KNN(k=1) mean=0.592 std=0.122 best=0.727
```

## Recap

- On imbalanced data, plain **accuracy** hides missed minority cases — always measure a `DummyClassifier` **baseline** first.
- A **confusion matrix** (`[[TN, FP], [FN, TP]]`) separates false alarms (`FP`) from missed positives (`FN`).
- **Precision** measures how reliable positive predictions are; **recall** measures how many real positives you caught; **F1** balances both (pass `zero_division=0` when zero positives may be predicted).
- `classification_report(..., digits=3)` shows per-class scores alongside `macro avg` (unweighted across classes) and `weighted avg` (weighted by `support`).
- Adjust the **decision threshold** on `.predict_proba(X)[:, 1]` to trade precision for recall without retraining the model.
- Use **cross-validation** (`cross_val_score` and `StratifiedKFold`) with preprocessing inside a `Pipeline`, and report `mean +/- std`.
