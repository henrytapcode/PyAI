# Plotting token usage by model

**What it shows:** how to turn the sorted SQL model report into a labelled bar chart and print a concise text summary of the top consumer.

**Step by step**
1. Lines 23–40 clean the logs, load them into SQLite, and fetch `model` and `total_tokens` sorted from highest to lowest.
2. Lines 42–48 draw a bar chart with `ax.bar(...)`, add a title and axis labels, and call `plt.show()`.
3. Lines 50–52 print the highest-token model and its total token count to standard output.

**Notice:** converting columns with `.tolist()` passes plain Python strings and integers to Matplotlib, keeping both the chart and summary print free of NumPy scalar formatting.

**Try it yourself:** plot `avg_latency` instead of `total_tokens` (and update the title and y-axis label) to compare model response speed visually.
