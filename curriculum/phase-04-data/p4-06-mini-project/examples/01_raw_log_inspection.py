# Inspect raw chatbot API logs to spot missing cells, messy model names, and duplicates.
import io
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
print("Shape:", df.shape)
print("Missing per column:")
print(df.isna().sum())
print("Raw model variants:", sorted(df["model"].unique().tolist()))
print("Duplicate request_ids:", int(df["request_id"].duplicated().sum()))
