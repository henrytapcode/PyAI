# Tune threshold on training CV, score the holdout test set once, and print an honest report.

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_val_score, train_test_split
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
logreg = make_pipeline(StandardScaler(), LogisticRegression())
tree = DecisionTreeClassifier(max_depth=3, random_state=0)
lr_cv = cross_val_score(logreg, X_train, y_train, cv=skf, scoring=f1_safe)
tr_cv = cross_val_score(tree, X_train, y_train, cv=skf, scoring=f1_safe)

oof_probs = cross_val_predict(logreg, X_train, y_train, cv=skf, method="predict_proba")[:, 1]
target_recall = 0.80
chosen_t = None
for t in [0.5, 0.4, 0.3, 0.2]:
    rec = float(recall_score(y_train, (oof_probs >= t).astype("int64")))
    if rec >= target_recall:
        chosen_t = t
        break

base = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
base_preds = base.predict(X_test)

lr_m, lr_s = round(float(lr_cv.mean()), 3), round(float(lr_cv.std()), 3)
tr_m, tr_s = round(float(tr_cv.mean()), 3), round(float(tr_cv.std()), 3)
print(f"test set: {len(y_test)} tickets ({int(y_test.sum())} urgent)")
print(f"baseline: acc={round(float(accuracy_score(y_test, base_preds)), 3):.3f} F1=0.000")
print(f"logreg CV F1: {lr_m:.3f} +/- {lr_s:.3f}")
print(f"tree   CV F1: {tr_m:.3f} +/- {tr_s:.3f}")
if chosen_t is None:
    print(f"no threshold reaches recall >= {target_recall:.2f}")
else:
    logreg.fit(X_train, y_train)
    test_preds = (logreg.predict_proba(X_test)[:, 1] >= chosen_t).astype("int64")
    print(f"chosen threshold (train OOF recall>={target_recall:.2f}): {chosen_t}")
    print("test confusion matrix:", confusion_matrix(y_test, test_preds).tolist())
    print(
        f"test metrics: prec={round(float(precision_score(y_test, test_preds, zero_division=0)), 3):.3f} "
        f"rec={round(float(recall_score(y_test, test_preds)), 3):.3f} "
        f"F1={round(float(f1_score(y_test, test_preds, zero_division=0)), 3):.3f}"
    )
if abs(lr_m - tr_m) < max(lr_s, tr_s):
    print("note: logreg and tree differ by less than one std; cannot claim one is clearly better")
