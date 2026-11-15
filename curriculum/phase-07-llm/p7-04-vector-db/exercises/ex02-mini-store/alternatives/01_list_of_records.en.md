# List of dataclass records with a scoring loop

Instead of stacking vectors into a 2-D NumPy matrix, this version stores each chunk as a `_Record` dataclass in a plain Python `list` and computes dot products with a `zip()` loop after filtering. Because Python's `.sort()` is stable, sorting by `-score` automatically preserves insertion order on ties. Deleting or updating a record only touches one list item with no `np.delete` array copy, though search becomes noticeably slower than vectorized `matrix @ q` once you store more than a few hundred chunks.
