# Aggregate API spend by model, sort descending, draw a bar chart, and print totals.
import matplotlib.pyplot as plt
import pandas as pd

logs = pd.DataFrame({
    "model": ["gpt-4o", "mini", "claude", "gpt-4o", "mini", "claude"],
    "cost": [2.40, 0.18, 1.55, 1.85, 0.22, 1.40],
})

totals = logs.groupby("model")["cost"].sum().sort_values(ascending=False)

fig, ax = plt.subplots()
ax.bar(totals.index.tolist(), totals.tolist())
ax.set_title("API cost by model")
ax.set_xlabel("model")
ax.set_ylabel("cost (USD)")
plt.show()

for model, total in totals.items():
    print(f"{model}: {float(total):.2f}")
