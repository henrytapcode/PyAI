# Clean raw API logs with pandas, aggregate per-model metrics in SQLite, and print each row.
import io
import sqlite3
import pandas as pd

csv_text = """request_id,model,tokens,latency_ms,status,rating
r01, GPT-4o,"1,200",850,ok,5
r02,gpt_4o,900,920,ok,4
r02,gpt_4o,950,999,error,1
r03,GPT-4o ,"1,100",N/A,error,
r04,gpt_4o,800,790,error,9
r05,gpt_4o,,600,ok,4
r06,Claude ,750,620,ok,5
r07,claude,650,580,ok,4
r08, CLAUDE,700,640,error,2
r09,claude ,500,timeout,ok,
r07,claude,999,700,ok,3
r10,mini,300,210,ok,4
r11, MINI ,250,190,ok,3
r12,mini,350,230,ok,5"""

df = pd.read_csv(io.StringIO(csv_text))
df["model"] = df["model"].str.strip().str.lower().str.replace("_", "-", regex=False)
df["tokens"] = pd.to_numeric(df["tokens"].astype(str).str.replace(",", "", regex=False), errors="coerce")
df["latency_ms"] = pd.to_numeric(df["latency_ms"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating"] = df["rating"].where(df["rating"].between(1, 5))
df = df.drop_duplicates(subset=["request_id"], keep="first")
df = df.dropna(subset=["tokens"]).reset_index(drop=True)
df["tokens"] = df["tokens"].astype("int64")

conn = sqlite3.connect(":memory:")
df.to_sql("requests", conn, index=False)
report = pd.read_sql_query("""
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
""", conn)
conn.close()

for _, row in report.iterrows():
    print(
        f"{row['model']:<7} req={row['requests']} tok={row['total_tokens']} "
        f"err={row['error_rate']} lat={row['avg_latency']} rat={row['avg_rating']}"
    )
