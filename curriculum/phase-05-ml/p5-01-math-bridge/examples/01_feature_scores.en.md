# Scoring requests with a dot product

**What it shows:** Using `@` to turn each request's feature vector and a shared weight vector into a single score, then picking the highest-scoring request.

**Step by step**
1. Lines 5–9 store each API request as a NumPy vector of three features: thousands of tokens, latency in seconds, and retry count.
2. Lines 11–12 define the model's `weights` (one weight per feature) and `bias`.
3. Lines 14–18 loop over the requests, compute `weights @ features + bias` as a Python `float`, and print each rounded score.
4. Lines 20–22 use `np.argmax(scores)` to find the index of the highest score and print its request ID.

**Notice:** `weights @ features` produces one number per request instead of an array, and wrapping the result in `float(...)` keeps Python formatting clean.

**Try it yourself:** Change the retry weight in `weights` from `0.8` to `3.0` and check how `req-102` and `req-103` scores jump compared to `req-101`.
