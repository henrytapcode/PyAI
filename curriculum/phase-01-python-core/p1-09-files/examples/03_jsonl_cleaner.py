# Save a config as JSON, then clean a JSON Lines dataset and write a cleaned copy.
import json
import tempfile
from pathlib import Path

config = {"min_length": 3, "note": "Xin chào"}
examples = [
    {"prompt": "Hi", "response": "Hello!"},
    {"prompt": "2+2?", "response": ""},
    {"prompt": "Hola", "response": "Xin chào bạn"},
    {"prompt": "Bye", "response": "ok"},
]

with tempfile.TemporaryDirectory() as tmp:
    config_path = Path(tmp) / "config.json"
    raw = Path(tmp) / "raw.jsonl"
    clean = Path(tmp) / "clean.jsonl"

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False)
    with open(config_path, encoding="utf-8") as f:
        settings = json.load(f)

    with open(raw, "w", encoding="utf-8") as f:
        for item in examples:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    kept = 0
    with open(raw, encoding="utf-8") as src, open(clean, "w", encoding="utf-8") as dst:
        for line in src:
            item = json.loads(line)
            if len(item["response"].strip()) >= settings["min_length"]:
                dst.write(json.dumps(item, ensure_ascii=False) + "\n")
                kept += 1

    print("kept", kept, "of", len(examples))
    for line in clean.read_text(encoding="utf-8").splitlines():
        print(json.loads(line)["prompt"])
