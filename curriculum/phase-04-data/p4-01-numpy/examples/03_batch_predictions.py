# Turn a 2D batch of class probabilities into predicted labels and count confident predictions.
import numpy as np

labels = ["negative", "neutral", "positive"]
probs = np.array([
    [0.05, 0.10, 0.85],
    [0.72, 0.20, 0.08],
    [0.10, 0.82, 0.08],
    [0.45, 0.35, 0.20],
])

pred_ids = probs.argmax(axis=1)
print("predicted ids:", pred_ids)
print("predicted labels:", [labels[int(i)] for i in pred_ids])

top_probs = probs.max(axis=1)
print("top confidence:", top_probs)

confident_count = int((top_probs >= 0.8).sum())
print("confident (>= 0.8):", confident_count)
