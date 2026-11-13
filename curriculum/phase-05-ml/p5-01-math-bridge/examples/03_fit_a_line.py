# Fit a straight line y = w * x + b to token-latency data with gradient descent and plot it.
import matplotlib.pyplot as plt
import numpy as np

tokens_k = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
latency_s = np.array([0.9, 1.4, 2.1, 2.6, 3.2])

w = 0.0
b = 0.0
lr = 0.04
losses = []

for _ in range(50):
    pred = w * tokens_k + b
    error = pred - latency_s
    losses.append(float(np.mean(error ** 2)))
    grad_w = float(np.mean(2 * error * tokens_k))
    grad_b = float(np.mean(2 * error))
    w = w - lr * grad_w
    b = b - lr * grad_b

final_loss = float(np.mean((w * tokens_k + b - latency_s) ** 2))
print(f"Fitted line: w={round(w, 2)}, b={round(b, 2)}")
print(f"Loss: start={round(losses[0], 3)}, end={round(final_loss, 3)}")

fig, ax = plt.subplots()
ax.scatter(tokens_k, latency_s, label="measured")
ax.plot(tokens_k, w * tokens_k + b, color="tab:orange", label="fitted line")
ax.set_title("Prompt size vs latency")
ax.set_xlabel("tokens (thousands)")
ax.set_ylabel("latency (s)")
ax.legend()
ax.grid(True)
plt.show()
