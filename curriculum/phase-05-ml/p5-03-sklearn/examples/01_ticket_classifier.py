# Classify support tickets as urgent (1) or normal (0) with LogisticRegression.
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(42)
normal = np.column_stack([rng.integers(20, 160, 12), rng.integers(0, 3, 12)]).astype(float)
urgent = np.column_stack([rng.integers(120, 320, 12), rng.integers(1, 6, 12)]).astype(float)
X = np.vstack([normal, urgent])
y = np.array([0] * 12 + [1] * 12)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
test_acc = round(model.score(X_test, y_test), 3)
print("Test accuracy:", test_acc)

new_tickets = np.array([[45.0, 0.0], [240.0, 4.0], [95.0, 1.0]])
preds = model.predict(new_tickets).tolist()
print("New ticket predictions:", preds)
