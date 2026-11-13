"""Mini-project part 2: build the SQL model report and plot token usage."""
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd


def model_report(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate cleaned logs by model in SQLite and return the sorted report DataFrame.

    Example:
        model_report(clean_df) -> columns
        ["model", "requests", "total_tokens", "error_rate", "avg_latency", "avg_rating"]
    """
    # TODO 1: open sqlite3.connect(":memory:") and write df via df.to_sql(...)
    # TODO 2: run one GROUP BY model query via pd.read_sql_query(...)
    # TODO 3: close conn before returning the sorted DataFrame
    return None


def plot_report(report: pd.DataFrame) -> tuple:
    """Draw a bar chart of total_tokens by model and return (fig, ax) without plt.show().

    Example:
        fig, ax = plot_report(report)
    """
    # TODO 4: create fig, ax = plt.subplots() and draw bars in report order
    # TODO 5: set title "Tokens by model", ylabel "tokens", and return (fig, ax)
    return None
