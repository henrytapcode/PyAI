# Inspect raw support ticket logs for missing cells, messy plans, duplicates, and class balance.

import numpy as np
import pandas as pd


def make_ticket_log(n=240, seed=21):
    rng = np.random.default_rng(seed)
    p0 = rng.choice(["free", "pro", "enterprise"], n, p=[0.45, 0.35, 0.20])
    tok, err = rng.integers(150, 2200, n).astype("float64"), rng.poisson(1.3, n).astype("float64")
    hrs = rng.uniform(0.5, 48.0, n).round(1)
    logit = -4.8 + 1.6 * err + 0.002 * tok - 0.08 * hrs + 1.2 * (p0 == "enterprise")
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype("int64")
    m = {"free": " Free", "pro": " PRO", "enterprise": "Enterprise "}
    plans = [m[str(p)] if i % 3 == 0 else str(p) for i, p in enumerate(p0)]
    tok_s = [f"{int(x):,}" if i % 6 == 0 else str(int(x)) for i, x in enumerate(tok)]
    tok_s[5], tok_s[37], tok_s[92], err[[12, 64]] = None, None, None, np.nan
    ids = [f"t{i:03d}" for i in range(n)]
    ids[20], ids[85], ids[140], ids[190] = ids[3], ids[11], ids[25], ids[44]
    leak = np.where(rng.random(n) < 0.98, y, 1 - y).astype("int64")
    return pd.DataFrame({
        "ticket_id": ids, "plan": plans, "tokens": tok_s, "error_count": err,
        "hours_since_deploy": hrs, "escalated_to_oncall": leak, "urgent": y,
    })


raw = make_ticket_log()
print("shape:", raw.shape)
print("duplicate ticket_id:", int(raw["ticket_id"].duplicated().sum()))
print("missing per column:")
for col in raw.columns:
    n_miss = int(raw[col].isna().sum())
    if n_miss > 0:
        print(f"  {col}: {n_miss}")

print("plan counts:")
for val, cnt in raw["plan"].value_counts().items():
    print(f"  {val!r}: {int(cnt)}")

n_urgent = int(raw["urgent"].sum())
print(f"urgent: {n_urgent}/{len(raw)} ({round(float(raw['urgent'].mean()), 3)})")
