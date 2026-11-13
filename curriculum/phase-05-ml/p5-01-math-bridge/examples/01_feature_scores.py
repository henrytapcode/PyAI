# Score three API requests with a weight vector using @ and find the highest-risk one.
import numpy as np

# Features per request: [tokens_in_k, latency_s, retries]
requests = [
    ("req-101", np.array([1.2, 0.4, 0.0])),
    ("req-102", np.array([4.5, 2.1, 2.0])),
    ("req-103", np.array([2.0, 0.8, 1.0])),
]

weights = np.array([0.4, 1.1, 0.8])
bias = -0.5

scores = []
for req_id, features in requests:
    score = float(weights @ features + bias)
    scores.append(score)
    print(f"{req_id}: {round(score, 3)}")

best_idx = int(np.argmax(scores))
best_id = requests[best_idx][0]
print(f"Highest score: {best_id} ({round(scores[best_idx], 3)})")
