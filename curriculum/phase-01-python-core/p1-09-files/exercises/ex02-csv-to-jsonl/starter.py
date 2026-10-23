"""Convert a CSV file (name,score) to a JSON Lines file.

Replace each ___ with the right word, then press Check.
"""
import csv
import json


def csv_to_jsonl(csv_path, jsonl_path):
    """Write each CSV row as one JSON object per line. Return the row count.

    Example: the row "Lan,9.5" becomes the line {"name": "Lan", "score": 9.5}
    """
    count = 0
    with open(csv_path, newline="", encoding="utf-8") as src:
        with open(jsonl_path, "___", encoding="utf-8") as dst:
            for row in csv.___(src):
                record = {"name": row["name"], "score": ___(row["score"])}
                dst.write(json.___(record, ensure_ascii=False) + "\n")
                count += 1
    return count
