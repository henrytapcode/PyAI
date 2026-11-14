# Scoring a batch of requests with a tensor

**What it shows:** Using matrix-vector multiplication (`@`) to score a `(4, 3)` batch of requests in one expression, then reading the rounded scores and top request index.

**Step by step**
1. Lines 5–10 pack four API requests (each with three features: thousands of tokens, latency in seconds, and message count) into one `(4, 3)` tensor.
2. Lines 11–12 define the shared `weights` vector of length `3` and scalar `bias`.
3. Line 14 computes all four scores at once with `requests @ weights + bias`, broadcasting `bias` across the batch.
4. Lines 15–19 extract the index of the maximum score with `.argmax().item()` and print `tuple(requests.shape)` plus rounded scores.

**Notice:** Calling `.tolist()` before rounding keeps the output free of raw tensor formatting, and `.argmax().item()` converts the 0-D index tensor into a plain Python `int`.

**Try it yourself:** Change the latency weight in `weights` from `1.1` to `0.1` and increase the message weight from `0.15` to `1.5`, then check how all four scores shift.
