import sqlite3
import matplotlib.pyplot as plt
import pandas as pd


def model_report(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate cleaned logs by model in SQLite and return the sorted report DataFrame."""
    conn = sqlite3.connect(":memory:")
    try:
        df.to_sql("requests", conn, index=False)
        sql = """
            SELECT
                model,
                COUNT(*) AS requests,
                SUM(tokens) AS total_tokens,
                ROUND(AVG(status = 'error'), 3) AS error_rate,
                ROUND(AVG(latency_ms), 1) AS avg_latency,
                ROUND(AVG(rating), 2) AS avg_rating
            FROM requests
            GROUP BY model
            ORDER BY total_tokens DESC, model ASC
        """
        return pd.read_sql_query(sql, conn)
    finally:
        conn.close()


def plot_report(report: pd.DataFrame) -> tuple:
    """Draw a bar chart of total_tokens by model and return (fig, ax)."""
    fig, ax = plt.subplots()
    ax.bar(report["model"].tolist(), report["total_tokens"].tolist())
    ax.set_title("Tokens by model")
    ax.set_ylabel("tokens")
    return fig, ax
