# Find ERROR lines in a log file one line at a time, without loading the whole file.
import tempfile
from pathlib import Path


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.strip()


def only_errors(lines):
    for line in lines:
        if "ERROR" in line:
            yield line


with tempfile.TemporaryDirectory() as tmp:
    log = Path(tmp) / "app.log"
    with open(log, "w", encoding="utf-8") as f:
        f.write("INFO model loaded\n")
        f.write("ERROR timeout after 30s\n")
        f.write("INFO request done\n")
        f.write("ERROR disk full\n")
        f.write("INFO request done\n")

    errors = only_errors(read_lines(log))
    print(next(errors))
    print(list(errors))

    total = sum(1 for line in only_errors(read_lines(log)))
    print("errors:", total)
