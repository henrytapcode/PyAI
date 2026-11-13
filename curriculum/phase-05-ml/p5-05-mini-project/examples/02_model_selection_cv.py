# Clean raw ticket logs, hold out a test split, and compare models with 5-fold stratified CV.

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
print("train/test rows:", len(X_train), len(X_test))

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
f1_safe = make_scorer(f1_score, zero_division=0)
models = [
    ("baseline", DummyClassifier(strategy="most_frequent")),
    ("logreg", make_pipeline(StandardScaler(), LogisticRegression())),
    ("tree", DecisionTreeClassifier(max_depth=3, random_state=0)),
]

print("model      mean    std")
best_name, best_mean = "", -1.0
for name, est in models:
    scores = cross_val_score(est, X_train, y_train, cv=skf, scoring=f1_safe)
    mean = round(float(scores.mean()), 3)
    std = round(float(scores.std()), 3)
    print(f"{name:<10} {mean:.3f}   {std:.3f}")
    if name != "baseline" and mean > best_mean:
        best_mean, best_name = mean, name

print("selected:", best_name)
