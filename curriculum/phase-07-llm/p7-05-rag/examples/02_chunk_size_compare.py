# Compare chunk sizes and overlaps on the same document and questions.
import numpy as np
from pyai_llm import FakeLLM

DOC = (
    "Welcome to our shop guide. "
    "Refunds are issued within 30 days of purchase with receipt. "
    "Standard shipping takes five business days across regions. "
    "Hardware warranty covers factory defects for twelve months."
)
TESTS = [
    ("How many days do refunds take?", "30 days"),
    ("How fast is standard shipping?", "five business days"),
    ("What does hardware warranty cover?", "factory defects"),
]


def chunk_words(text: str, size: int, overlap: int) -> list[str]:
    words = text.split()
    step = size - overlap
    chunks: list[str] = []
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i : i + size]))
        if i + size >= len(words):
            break
        i += step
    return chunks


client = FakeLLM(embed_dim=256)
print(f"{'size/ov':<8} {'chunks':>6} {'hits':>6}")
print("-" * 22)
for size, overlap in [(5, 0), (8, 0), (8, 3), (12, 3)]:
    chunks = chunk_words(DOC, size, overlap)
    matrix = np.array(client.embed(chunks), dtype=float)
    found = 0
    for q, needle in TESTS:
        qv = np.array(client.embed([q])[0], dtype=float)
        best = int(np.argsort(-(matrix @ qv), kind="stable")[0])
        if needle in chunks[best]:
            found += 1
    print(f"{f'{size}/{overlap}':<8} {len(chunks):>6} {f'{found}/{len(TESTS)}':>6}")
