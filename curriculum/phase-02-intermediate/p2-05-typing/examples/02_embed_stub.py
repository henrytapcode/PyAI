# A fake embedding function with full type hints, and a call that breaks the hint.
def embed(texts: list[str]) -> list[list[float]]:
    vectors = []
    for text in texts:
        vectors.append([float(len(text)), float(text.count("a"))])
    return vectors


def dot(a: list[float], b: list[float]) -> float:
    total = 0.0
    for i in range(len(a)):
        total += a[i] * b[i]
    return total


vectors = embed(["banana", "apple"])
print(vectors)
print(dot(vectors[0], vectors[1]))

# Wrong on purpose: one str instead of a list[str]. Python does not complain.
print(embed("cat"))
print(embed.__annotations__)
