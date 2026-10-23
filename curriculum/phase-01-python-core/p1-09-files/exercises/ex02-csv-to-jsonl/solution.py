import csv
import json


def csv_to_jsonl(csv_path, jsonl_path):
    count = 0
    with open(csv_path, newline="", encoding="utf-8") as src:
        with open(jsonl_path, "w", encoding="utf-8") as dst:
            for row in csv.DictReader(src):
                record = {"name": row["name"], "score": float(row["score"])}
                dst.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
    return count
