Fill in the `___` blanks inside `plot_loss(epochs, losses)` so it draws a line chart of training loss over epochs and returns `(fig, ax)`. Write your code inside the function and `return` the `(fig, ax)` tuple without calling `plt.show()`.

**Example**

```python
fig, ax = plot_loss([1, 2, 3], [0.9, 0.5, 0.3])
ax.get_title()    # "Training loss"
ax.get_xlabel()   # "epoch"
ax.get_ylabel()   # "loss"
```

**Rules**

- Create the plot with `plt.subplots()`.
- Plot `epochs` vs `losses` with `label="loss"` and `marker="o"`.
- Set the title `"Training loss"`, x-axis label `"epoch"`, and y-axis label `"loss"`.
- Display the legend with `ax.legend()`.
- Do not call `plt.show()` inside `plot_loss`.
