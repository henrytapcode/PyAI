# Group model evaluation scores and find the highest-scoring model.
import pandas as pd

evals = pd.DataFrame({
    "model": ["gpt-4o", "claude", "llama", "gpt-4o", "claude", "llama"],
    "task": ["qa", "qa", "qa", "code", "code", "code"],
    "score": [0.91, 0.88, 0.76, 0.89, 0.94, 0.80],
})

summary = evals.groupby("model")["score"].agg(["mean", "count"]).round(2)
summary = summary.sort_values("mean", ascending=False)
print(summary)

best_model = str(summary.index[0])
best_score = float(summary.iloc[0]["mean"])
print("Best model:", best_model, best_score)
