# Fit polynomial degrees 1, 3, and 6 on noisy train points, print train/test MSE, and plot all three curves.
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(27)
x = np.linspace(0.0, 1.0, 12)
y = 0.5 + 4.0 * x * (1.0 - x) + rng.normal(0.0, 0.12, size=len(x))

idx = rng.permutation(len(x))
x_train, x_test = x[idx[:8]], x[idx[8:]]
y_train, y_test = y[idx[:8]], y[idx[8:]]

grid = np.linspace(0.0, 1.0, 100)
fig, ax = plt.subplots()
ax.scatter(x_train, y_train, label="train")
ax.scatter(x_test, y_test, marker="s", label="test")

for deg in [1, 3, 6]:
    coeffs = np.polyfit(x_train, y_train, deg)
    train_mse = float(np.mean((np.polyval(coeffs, x_train) - y_train) ** 2))
    test_mse = float(np.mean((np.polyval(coeffs, x_test) - y_test) ** 2))
    print(f"degree={deg}  train_mse={round(train_mse, 3)}  test_mse={round(test_mse, 3)}")
    ax.plot(grid, np.polyval(coeffs, grid), label=f"degree {deg}")

ax.set_title("Overfitting: degree 1 vs 3 vs 6")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
ax.grid(True)
plt.show()
