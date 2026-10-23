# Write scores to a CSV file, read them back and compute each student's average.
import csv
import tempfile
from pathlib import Path

rows = [
    {"name": "Lan", "score": 9.5},
    {"name": "Minh", "score": 7},
    {"name": "Lan", "score": 8.5},
    {"name": "Minh", "score": 8},
]

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "scores.csv"

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "score"])
        writer.writeheader()
        writer.writerows(rows)

    totals = {}
    counts = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row["name"]
            score = float(row["score"])
            if name in totals:
                totals[name] += score
                counts[name] += 1
            else:
                totals[name] = score
                counts[name] = 1

    for name in totals:
        print(f"{name}: {totals[name] / counts[name]:.2f}")
