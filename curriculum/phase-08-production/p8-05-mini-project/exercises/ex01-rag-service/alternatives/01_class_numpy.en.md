# Class-based RagService with NumPy matrix scoring

**How it works:** Instead of keeping `doc_vecs` in closure variables and looping with Python `cosine`, this alternative wraps indexing and retrieval inside a `RagService` class backed by a 2D NumPy array and `np.argsort(-scores, kind="stable")`.

**When to choose it:** This structure scales cleanly as corpora grow (vectorized matrix-vector multiplication is much faster than a Python loop over thousands of documents) and keeps FastAPI routes thin, at the cost of adding a NumPy dependency and slightly more boilerplate for small corpora.
