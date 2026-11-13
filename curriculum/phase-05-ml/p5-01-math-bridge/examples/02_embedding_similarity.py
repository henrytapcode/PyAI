# Rank short 4D document embeddings against a query using cosine similarity.
import numpy as np

query = np.array([0.9, 0.4, 0.1, 0.0])

docs = [
    ("refund_policy", np.array([0.8, 0.5, 0.1, 0.0])),
    ("api_pricing", np.array([0.1, 0.2, 0.9, 0.4])),
    ("shipping_faq", np.array([0.5, 0.4, 0.3, 0.2])),
    ("dark_mode_ui", np.array([0.0, 0.1, 0.2, 0.9])),
]

best_name = ""
best_sim = -2.0
q_norm = np.linalg.norm(query)

for name, vec in docs:
    sim = float((query @ vec) / (q_norm * np.linalg.norm(vec)))
    print(f"{name}: {round(sim, 3)}")
    if sim > best_sim:
        best_sim = sim
        best_name = name

print(f"Closest doc: {best_name} ({round(best_sim, 3)})")
