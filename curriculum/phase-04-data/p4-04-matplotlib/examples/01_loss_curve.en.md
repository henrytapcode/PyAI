# Training and validation loss curve

**What it shows:** plotting two lines (`train_loss` and `val_loss`) on the same `Axes` with markers, axis labels, a legend, and gridlines, then finding the epoch with the lowest validation loss.

**Step by step**
1. Lines 4–6 define six epochs along with their training and validation losses.
2. Lines 8–10 create a `(fig, ax)` pair with `plt.subplots()` and plot both curves using `marker="o"` and `label=` names.
3. Lines 11–16 set the title, axis labels, legend, and grid, then call `plt.show()`.
4. Lines 18–19 locate the index of `min(val_loss)` and print the best epoch.

**Notice:** each `ax.plot(...)` call must pass `label=` before `ax.legend()` is called, otherwise the legend stays empty.

**Try it yourself:** add a 7th epoch with `train_loss` `0.21` and `val_loss` `0.49` and check how the chart and the printed best epoch update.
