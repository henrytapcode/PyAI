# Scatter plot of prompt tokens vs response latency for 8 requests and print correlation.
import matplotlib.pyplot as plt
import numpy as np

tokens = np.array([120, 240, 310, 480, 560, 720, 890, 1050])
latency_ms = np.array([210, 240, 330, 390, 475, 535, 710, 790])

fig, ax = plt.subplots()
ax.scatter(tokens, latency_ms)
ax.set_title("Prompt tokens vs latency")
ax.set_xlabel("tokens")
ax.set_ylabel("latency (ms)")
ax.grid(True)
plt.show()

corr = round(float(np.corrcoef(tokens, latency_ms)[0, 1]), 2)
print("Correlation:", corr)
