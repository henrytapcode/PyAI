# Compare unscaled KNN with a StandardScaler + KNN pipeline on mismatched scales.
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(7)
tokens = rng.integers(200, 4000, size=40).astype(float)
error_rate = np.concatenate([rng.uniform(0.0, 0.12, 20), rng.uniform(0.18, 0.45, 20)])
X = np.column_stack([tokens, error_rate])
y = np.array([0] * 20 + [1] * 20)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

raw_knn = KNeighborsClassifier(n_neighbors=3)
raw_knn.fit(X_train, y_train)
raw_acc = round(raw_knn.score(X_test, y_test), 3)

scaled_pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
scaled_pipe.fit(X_train, y_train)
pipe_acc = round(scaled_pipe.score(X_test, y_test), 3)

print("KNN without scaling:", raw_acc)
print("Pipeline with StandardScaler:", pipe_acc)
