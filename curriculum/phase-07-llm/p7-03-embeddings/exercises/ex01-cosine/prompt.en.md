Complete `cosine_sim(a, b)` in `starter.py` by replacing every `___` blank so it computes cosine similarity between two numeric lists using NumPy.

Write your code inside the function and `return` the rounded `float` result.

## Example

```python
cosine_sim([3.0, 4.0], [6.0, 8.0])   # -> 1.0
cosine_sim([1.0, 0.0], [0.0, 1.0])   # -> 0.0
cosine_sim([0.0, 0.0], [1.0, 2.0])   # -> 0.0
```

## Rules

- Raise `ValueError` if `a` and `b` do not have the same length.
- Return `0.0` if either vector is an all-zero vector (or empty).
- Use NumPy to compute vector norms and the dot product.
- Return a Python `float` rounded to 3 decimal places.
