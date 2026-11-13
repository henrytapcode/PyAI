# Filter low-rated chatbot sessions and sort them by rating.
import pandas as pd

logs = pd.DataFrame({
    "user": ["an", "binh", "chi", "dung", "emily"],
    "messages": [4, 12, 3, 9, 7],
    "rating": [5, 2, 4, 1, 2],
})

print("Total sessions:", len(logs))
low = logs[logs["rating"] <= 2].sort_values(
    ["rating", "messages"], ascending=[True, False]
).reset_index(drop=True)

print("Low-rated sessions:")
print(low)
