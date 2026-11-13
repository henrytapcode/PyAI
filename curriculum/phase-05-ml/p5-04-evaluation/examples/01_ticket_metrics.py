# Compare a baseline and LogisticRegression using confusion matrix, precision, recall, and F1.

import numpy as np
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
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

base_preds = baseline.predict(X_test)
model_preds = pipe.predict(X_test)

print("test counts:", np.bincount(y_test, minlength=2).tolist())
print("baseline acc:", round(float(baseline.score(X_test, y_test)), 3))
print(
    "baseline recall:",
    round(float(recall_score(y_test, base_preds, zero_division=0)), 3),
)
print("model acc:", round(float(pipe.score(X_test, y_test)), 3))
print("confusion matrix:", confusion_matrix(y_test, model_preds).tolist())
print(
    "precision / recall / f1:",
    round(float(precision_score(y_test, model_preds)), 3),
    round(float(recall_score(y_test, model_preds)), 3),
    round(float(f1_score(y_test, model_preds)), 3),
)
print(classification_report(y_test, model_preds, digits=3))
