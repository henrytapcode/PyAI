# One logger, two destinations: short messages on screen, every detail in a file.
import logging
import sys
import tempfile

logger = logging.getLogger("pipeline")
logger.setLevel(logging.DEBUG)
logger.propagate = False

console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(levelname)s %(message)s"))


def embed_batch(texts):
    vectors = []
    number = 0
    for text in texts:
        number += 1
        logger.debug("embedding text %d (%d characters)", number, len(text))
        if len(text) > 20:
            logger.warning("text %d is long and may be cut", number)
        vectors.append(len(text))
    logger.info("embedded %d texts", len(vectors))
    return vectors


with tempfile.TemporaryDirectory() as tmp:
    log_path = f"{tmp}/pipeline.log"
    to_file = logging.FileHandler(log_path, encoding="utf-8")
    to_file.setLevel(logging.DEBUG)
    to_file.setFormatter(logging.Formatter("%(levelname)s %(funcName)s %(message)s"))

    handlers = [console, to_file]
    for handler in handlers:
        logger.addHandler(handler)
    try:
        embed_batch(["hello", "a very long document about vector databases", "bye"])
    finally:
        for handler in handlers:
            logger.removeHandler(handler)
            handler.close()

    print("--- file ---")
    with open(log_path, encoding="utf-8") as f:
        for line in f.read().splitlines():
            print(line)
