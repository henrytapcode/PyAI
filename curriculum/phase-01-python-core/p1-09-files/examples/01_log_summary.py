# Write a log file, append to it, then count the lines per level.
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    log = Path(tmp) / "app.log"

    with open(log, "w", encoding="utf-8") as f:
        f.write("INFO model loaded\n")
        f.write("ERROR timeout\n")
    with open(log, "a", encoding="utf-8") as f:
        f.write("INFO request done\n")
        f.write("INFO request done\n")

    counts = {}
    with open(log, encoding="utf-8") as f:
        for line in f:
            level = line.strip().split(" ")[0]
            if level in counts:
                counts[level] += 1
            else:
                counts[level] = 1

    print(log.name, log.suffix)
    print(counts)
