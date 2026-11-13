# API cost by model

**What it shows:** grouping API spend by model in pandas, sorting totals in descending order, drawing a bar chart with `ax.bar()`, and printing formatted totals.

**Step by step**
1. Lines 5–8 build a DataFrame with six API request rows across three models.
2. Line 10 sums `cost` per `model` with `.groupby("model")["cost"].sum()` and sorts from highest to lowest.
3. Lines 12–17 create `(fig, ax)`, draw bars from `totals.index.tolist()` and `totals.tolist()`, add labels, and call `plt.show()`.
4. Lines 19–20 print each model's total formatted to two decimal places.

**Notice:** passing `.tolist()` turns the pandas Index and values into plain Python lists, avoiding NumPy scalar types when inspecting or printing.

**Try it yourself:** change `ax.bar(...)` on line 13 to `ax.barh(...)` (and swap the x/y axis labels) to see how horizontal bars look.
