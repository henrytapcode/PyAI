# Pure Python ranking with `cosine()` and `sorted()`

This alternative avoids NumPy completely by keeping embeddings as plain lists of floats, scoring each chunk with `pyai_llm.cosine(vec, q_vec)`, and sorting `(score, idx)` pairs with `(-score, idx)` so ties break by earlier index. It is easy to read and works even in minimal environments without NumPy, while the NumPy matrix dot product in `solution.py` is much faster once an index grows past a few thousand chunks.
