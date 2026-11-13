import matplotlib.pyplot as plt
import pandas as pd


def cost_bar_chart(df: pd.DataFrame) -> tuple:
    """Sum API cost by model, sort descending, draw a bar chart, and return (fig, ax).

    Example: fig, ax = cost_bar_chart(pd.DataFrame({"model": ["a", "b"], "cost": [1.0, 2.5]}))
    """
    # TODO: group by "model", sum "cost", and sort descending
    # TODO: create (fig, ax), draw bars, and set title "Cost by model" and ylabel "cost (USD)"
    fig, ax = plt.subplots()
    return fig, ax
