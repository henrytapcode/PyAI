# Sweep decision thresholds on predict_proba to balance precision and recall.

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

thresholds = [0.5, 0.4, 0.3, 0.2, 0.1]
best_threshold = None

print(f"{'threshold':>9} {'precision':>9} {'recall':>7} {'urgent':>7}")
for t in thresholds:
    preds = (probs >= t).astype("int64")
    prec = round(float(precision_score(y_test, preds, zero_division=0)), 3)
    rec = round(float(recall_score(y_test, preds)), 3)
    urgent = int(preds.sum())
    print(f"{t:>9.1f} {prec:>9.3f} {rec:>7.3f} {urgent:>7d}")
    if rec >= 0.8 and (best_threshold is None or t > best_threshold):
        best_threshold = t

print("highest threshold with recall >= 0.8:", best_threshold)
