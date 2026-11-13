import matplotlib.pyplot as plt
import pandas as pd


def cost_bar_chart(df: pd.DataFrame) -> tuple:
    """Sum API cost by model, sort descending, draw a bar chart, and return (fig, ax).

    Example: fig, ax = cost_bar_chart(pd.DataFrame({"model": ["a", "b"], "cost": [1.0, 2.5]}))
    """
    totals = df.groupby("model")["cost"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.bar(totals.index.tolist(), totals.tolist())
    ax.set_title("Cost by model")
    ax.set_ylabel("cost (USD)")
    return fig, ax
