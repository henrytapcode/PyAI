# Compare three model pipelines using 5-fold stratified cross-validation.

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

X, y = load_breast_cancer(return_X_y=True)
print("dataset shape:", X.shape, "class counts:", np.bincount(y).tolist())

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
candidates = [
    ("LogReg", LogisticRegression(max_iter=1000)),
    ("KNN(k=5)", KNeighborsClassifier(n_neighbors=5)),
    ("Tree(d=4)", DecisionTreeClassifier(max_depth=4, random_state=0)),
]

best_name = ""
best_mean = -1.0

for name, estimator in candidates:
    pipe = make_pipeline(StandardScaler(), estimator)
    scores = cross_val_score(pipe, X, y, cv=skf, scoring="f1")
    mean = round(float(scores.mean()), 3)
    std = round(float(scores.std()), 3)
    print(f"{name:<10} mean={mean:.3f} std={std:.3f}")
    if mean > best_mean:
        best_mean = mean
        best_name = name

print("best model:", best_name, "with F1", best_mean)
