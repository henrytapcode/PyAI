# Check sensor temperatures with summary stats and boolean masks.
import numpy as np

temps_c = np.array([22.5, 23.1, 41.8, 22.9, 19.4, -5.0, 23.4])
print("min:", temps_c.min())
print("max:", temps_c.max())
print("mean:", round(float(temps_c.mean()), 2))

outliers = temps_c[(temps_c < 10) | (temps_c > 35)]
print("outliers:", outliers)

normal = temps_c[(temps_c >= 10) & (temps_c <= 35)]
print("normal count:", len(normal))
print("clean mean:", round(float(normal.mean()), 2))
