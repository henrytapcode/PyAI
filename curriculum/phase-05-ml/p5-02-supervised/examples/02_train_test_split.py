# Shuffle and split a 10-row request DataFrame 80/20, fit a line on train via gradient descent, and check test MSE.
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "id": list(range(1, 11)),
    "tokens": [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000],
    "latency": [0.55, 0.82, 1.05, 1.38, 1.60, 1.95, 2.18, 2.50, 2.72, 3.05],
})

rng = np.random.default_rng(42)
idx = rng.permutation(len(df))
train_idx, test_idx = idx[:8], idx[8:]

ids = df["id"].to_numpy()
print("Train IDs:", ids[train_idx].tolist())
print("Test IDs:", ids[test_idx].tolist())

x = df["tokens"].to_numpy() / 1000.0
y = df["latency"].to_numpy()
x_train, y_train = x[train_idx], y[train_idx]
x_test, y_test = x[test_idx], y[test_idx]

w, b, lr = 0.0, 0.0, 0.04
for _ in range(50):
    error = (w * x_train + b) - y_train
    w = w - lr * float(np.mean(2 * error * x_train))
    b = b - lr * float(np.mean(2 * error))

train_mse = float(np.mean((w * x_train + b - y_train) ** 2))
test_mse = float(np.mean((w * x_test + b - y_test) ** 2))
print(f"Fitted line: w={round(w, 3)}, b={round(b, 3)}")
print(f"Train MSE={round(train_mse, 3)}, Test MSE={round(test_mse, 3)}")
