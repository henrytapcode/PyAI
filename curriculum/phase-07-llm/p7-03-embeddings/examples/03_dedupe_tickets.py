# Find near-duplicate support tickets from the upper triangle of D @ D.T.
import numpy as np
from pyai_llm import FakeLLM

TICKETS = [
    "Laptop screen shows startup error",
    "Notebook displays startup bug",
    "Quick car pickup at terminal",
    "Fast vehicle pickup at terminal",
    "Refund delayed for damaged kitten toy",
]

THRESHOLD = 0.5

client = FakeLLM(embed_dim=256)
matrix = np.array(client.embed(TICKETS))
sim_matrix = matrix @ matrix.T

print("Duplicate pairs (cosine >= 0.5):")
n_tickets = len(TICKETS)
for i in range(n_tickets):
    for j in range(i + 1, n_tickets):
        score = round(float(sim_matrix[i, j]), 3)
        if score >= THRESHOLD:
            print(f"  ({i}, {j}) score={score}: {TICKETS[i]} <-> {TICKETS[j]}")
