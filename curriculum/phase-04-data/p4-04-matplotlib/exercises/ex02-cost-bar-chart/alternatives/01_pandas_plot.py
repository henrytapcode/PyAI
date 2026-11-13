import matplotlib.pyplot as plt
import pandas as pd


def cost_bar_chart(df: pd.DataFrame) -> tuple:
    """Sum API cost by model, sort descending, plot with pandas, and return (fig, ax)."""
    totals = df.groupby("model")["cost"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots()
    totals.plot(kind="bar", ax=ax)
    ax.set_title("Cost by model")
    ax.set_ylabel("cost (USD)")
    return fig, ax
