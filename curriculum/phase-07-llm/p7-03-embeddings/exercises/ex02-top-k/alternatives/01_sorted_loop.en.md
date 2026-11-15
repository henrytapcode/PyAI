# Loop with cosine() and sorted()

**How it works:** Instead of converting embeddings into a NumPy matrix for `D @ q` and `np.argsort`, this version loops over `doc_vecs`, scores each one with `pyai_llm.cosine()`, filters by `min_score`, and sorts pairs with `key=lambda pair: (-pair[1], pair[0])`.

**When to choose it:** Great when you already have plain Python lists, want zero NumPy dependency, or want explicit control over non-normalized vectors (since `cosine()` divides by vector norms automatically). For thousands of documents, the vectorized `D @ q` solution is much faster.
