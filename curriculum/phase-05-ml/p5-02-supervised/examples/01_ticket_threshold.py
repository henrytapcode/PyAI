# Search candidate thresholds on 12 support tickets and pick the highest accuracy.
import numpy as np

scores = np.array([0.12, 0.18, 0.27, 0.34, 0.48, 0.52, 0.59, 0.64, 0.71, 0.78, 0.86, 0.94])
labels = np.array([0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1])

best_t = 0.0
best_acc = -1.0

for t in [0.25, 0.4, 0.55, 0.7, 0.85]:
    preds = (scores >= t).astype("int64")
    acc = float((preds == labels).mean())
    print(f"threshold={t:.2f}  accuracy={round(acc, 3)}")
    if acc > best_acc:
        best_acc = acc
        best_t = t

print(f"Best threshold: {best_t:.2f} (accuracy={round(best_acc, 3)})")
