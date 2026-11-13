# Read API usage from CSV, compute total tokens and cost, and print the top 3.
import io
import pandas as pd

csv_data = """model,prompt_tokens,completion_tokens
gpt-4o,800,400
claude,1200,600
llama,500,300
gpt-4o,1500,900
claude,400,200"""

df = pd.read_csv(io.StringIO(csv_data))
df["total_tokens"] = df["prompt_tokens"] + df["completion_tokens"]
df["cost"] = (df["total_tokens"] * 0.002 / 1000).round(4)

top3 = df.sort_values("cost", ascending=False).reset_index(drop=True).head(3)
print("Top 3 most expensive calls:")
print(top3[["model", "total_tokens", "cost"]])
print("Total cost:", round(float(df["cost"].sum()), 4))
