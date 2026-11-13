# Plot training and validation loss curves across 6 epochs and print the best epoch.
import matplotlib.pyplot as plt

epochs = [1, 2, 3, 4, 5, 6]
train_loss = [0.92, 0.68, 0.51, 0.39, 0.31, 0.25]
val_loss = [0.95, 0.72, 0.58, 0.54, 0.59, 0.67]

fig, ax = plt.subplots()
ax.plot(epochs, train_loss, marker="o", label="train_loss")
ax.plot(epochs, val_loss, marker="o", label="val_loss")
ax.set_title("Training vs validation loss")
ax.set_xlabel("epoch")
ax.set_ylabel("loss")
ax.legend()
ax.grid(True)
plt.show()

best_idx = val_loss.index(min(val_loss))
print(f"Best epoch: {epochs[best_idx]} (val_loss={val_loss[best_idx]})")
