# Stage 3: a ledger context manager appends calls safely, then we summarise cost by model and day.
import json
import tempfile
from contextlib import contextmanager
from pathlib import Path


def load_rows(path):
    return json.loads(path.read_text(encoding="utf-8"))


@contextmanager
def ledger(path):
    rows = load_rows(path) if path.exists() else []
    yield rows
    path.write_text(json.dumps(rows), encoding="utf-8")


def cost_by(rows, field):
    totals = {}
    for row in rows:
        key = row[field]
        totals[key] = totals.get(key, 0) + row["cost"]
    return {key: round(totals[key], 4) for key in sorted(totals)}


with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "ledger.json"

    with ledger(path) as rows:
        rows.append({"day": "2024-05-01", "model": "small", "cost": 0.002})
        rows.append({"day": "2024-05-01", "model": "large", "cost": 0.04})

    with ledger(path) as rows:
        rows.append({"day": "2024-05-02", "model": "small", "cost": 0.0005})
        rows.append({"day": "2024-05-02", "model": "mid", "cost": 0.04})

    try:
        with ledger(path) as rows:
            rows.append({"day": "2024-05-03", "model": "large", "cost": 9.99})
            raise RuntimeError("crash before the session ended")
    except RuntimeError as err:
        print("error:", err)

    rows = load_rows(path)
    print("rows saved:", len(rows))
    for model, total in cost_by(rows, "model").items():
        print(f"{model}: {total:.4f}")
    for day, total in cost_by(rows, "day").items():
        print(f"{day}: {total:.4f}")

    # Ties: ">=" lets a later name replace an earlier one with the same total.
    biggest = ""
    biggest_total = 0.0
    for model, total in cost_by(rows, "model").items():
        if total >= biggest_total:
            biggest = model
            biggest_total = total
    print("most expensive model:", biggest)
    tied = [m for m, t in cost_by(rows, "model").items() if t == biggest_total]
    print("tied at the top:", tied)
