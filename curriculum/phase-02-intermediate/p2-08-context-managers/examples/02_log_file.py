# A class-based context manager that writes a log file and always closes it.
import tempfile


class LogFile:
    def __init__(self, path):
        self.path = path
        self.file = None

    def __enter__(self):
        self.file = open(self.path, "w", encoding="utf-8")
        print("log opened")
        return self

    def log(self, message):
        self.file.write(message + "\n")

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        print("log closed")
        return False


with tempfile.TemporaryDirectory() as tmp:
    path = f"{tmp}/run.log"

    with LogFile(path) as run:
        run.log("start")
        run.log("embedded 3 documents")
    print("closed:", run.file.closed)

    try:
        with LogFile(path) as run:
            run.log("start again")
            raise RuntimeError("api down")
    except RuntimeError as err:
        print("error:", err)
    print("closed:", run.file.closed)

    with open(path, encoding="utf-8") as f:
        print(f.read().splitlines())
