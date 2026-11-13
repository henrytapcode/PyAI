# Clean a user survey table: count missing cells, drop missing users, fill score gaps.
import io
import pandas as pd

csv_text = """user,plan,score
an,pro,5
,free,2
binh,pro,
chi,free,4
dung,pro,
em,free,3"""

df = pd.read_csv(io.StringIO(csv_text))
print("Missing per column:")
print(df.isna().sum())

cleaned = df.dropna(subset=["user"]).reset_index(drop=True)
median_score = float(cleaned["score"].median())
cleaned["score"] = cleaned["score"].fillna(median_score)

print("Cleaned survey:")
print(cleaned)
print("Average score:", round(float(cleaned["score"].mean()), 2))
