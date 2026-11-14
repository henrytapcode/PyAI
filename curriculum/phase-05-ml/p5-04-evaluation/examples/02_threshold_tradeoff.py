# Tune the decision threshold on a validation split from train, then score test once.

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(
    n_samples=200, n_features=5, weights=[0.85], random_state=1
)
X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0, stratify=y
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full, test_size=0.25, random_state=0, stratify=y_train_full
)

pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)
val_probs = pipe.predict_proba(X_val)[:, 1]

thresholds = [0.5, 0.4, 0.3, 0.2, 0.1]
target_recall = 0.8
best_threshold = None

print(f"{'threshold':>9} {'precision':>9} {'recall':>7} {'urgent':>7}")
for t in thresholds:
    preds = (val_probs >= t).astype("int64")
    prec = round(float(precision_score(y_val, preds, zero_division=0)), 3)
    rec = round(float(recall_score(y_val, preds)), 3)
    urgent = int(preds.sum())
    print(f"{t:>9.1f} {prec:>9.3f} {rec:>7.3f} {urgent:>7d}")
    if rec >= target_recall and (best_threshold is None or t > best_threshold):
        best_threshold = t

print(f"chosen on val (recall >= {target_recall}):", best_threshold)
if best_threshold is None:
    print(f"no threshold reaches recall >= {target_recall} on val")
else:
    test_probs = pipe.predict_proba(X_test)[:, 1]
    test_preds = (test_probs >= best_threshold).astype("int64")
    test_prec = round(float(precision_score(y_test, test_preds, zero_division=0)), 3)
    test_rec = round(float(recall_score(y_test, test_preds)), 3)
    print(f"test once (t={best_threshold}): precision={test_prec} recall={test_rec}")
