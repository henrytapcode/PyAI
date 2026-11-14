# Score a batch of four API requests at once with @ and find the highest-scoring row.
import torch

# Features per request: [tokens_in_k, latency_s, messages]
requests = torch.tensor([
    [1.2, 0.4, 2.0],
    [4.5, 2.1, 8.0],
    [2.0, 0.8, 3.0],
    [3.1, 1.3, 5.0],
])
weights = torch.tensor([0.4, 1.1, 0.15])
bias = -0.5

scores = requests @ weights + bias
best_idx = scores.argmax().item()

print("shape:", tuple(requests.shape))
print("scores:", [round(v, 3) for v in scores.tolist()])
print("highest_idx:", best_idx)
