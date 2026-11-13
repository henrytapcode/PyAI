Write `cost_bar_chart(df)` to aggregate total API `cost` per `model`, sort the models in descending order of total cost, draw a bar chart on `ax`, and return `(fig, ax)`. Write your code inside the function and `return` the `(fig, ax)` tuple without calling `plt.show()`.

**Example**

```python
df = pd.DataFrame({
    "model": ["mini", "gpt-4o", "mini", "claude"],
    "cost": [0.15, 4.25, 0.25, 2.95],
})
fig, ax = cost_bar_chart(df)
# Bars left-to-right: "gpt-4o" (4.25), "claude" (2.95), "mini" (0.40)
```

**Rules**

- Each `model` must appear at most once on the chart (sum repeated rows).
- Sort bars from highest total cost to lowest.
- Set the title to `"Cost by model"` and the y-axis label to `"cost (USD)"`.
- Do not modify the input DataFrame `df` in place, and do not call `plt.show()`.
